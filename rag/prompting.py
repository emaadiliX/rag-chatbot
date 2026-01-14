from __future__ import annotations

import re
from typing import Dict, Any, List

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from .retrieval import retrieve_context, format_retrieved_context

load_dotenv()

IDK_FALLBACK = "I don't have enough information in the provided documents to answer this question."

SYSTEM_PROMPT = """You are a professional banking and regulatory assistant.

Guidelines:
- Use ONLY the provided context to answer. 
- You are strictly grounded: do not use outside knowledge.
- If the context describes a role, person, or entity (the subject), but does NOT mention a specific capability, action, or fact asked about in the question, you should:
  1. Describe what is known about the subject's role or duties based on the context.
  2. State clearly that the specific capability or action (e.g., "setting interest rates") is not mentioned in the provided documents or is not part of the described role.
- Be conversational, professional, and helpful.
- Use [Source N] citations for your claims.
- If the context is entirely unrelated to any aspect of the question (different subjects, different topics), use the fallback phrase: "I don't have enough information in the provided documents to answer this question."
"""

USER_PROMPT = """Context:
{context}

Question: {question}

Instructions:
1. Provide a direct answer.
2. If the user asks about a specific power or duty: first summarize the duties described in the context, then clarify if the specific power/duty is absent or specifically excluded based on those documents.
3. Cite sources using [Source N] markers.
4. Only use the "I don't have enough information..." fallback if the documents provide no information at all about the entities or topics in the question.

Answer:
"""


def _looks_like_prompt_injection(text: str) -> bool:
    if not text:
        return False
    patterns = [
        r"ignore (all|any|previous) instructions",
        r"system prompt",
        r"developer message",
        r"you are chatgpt",
        r"reveal.*(prompt|policy|instructions)",
        r"do not follow",
        r"override",
        r"forget your",          
        r"new instructions",    
        r"disregard", 
    ]
    return any(re.search(p, text, flags=re.IGNORECASE) for p in patterns)


def _build_sources_list(citations: List[Dict[str, Any]]) -> List[str]:
    sources = []
    seen = set()
    for c in citations:
        src = c.get("source", "Unknown")
        page = c.get("page", "?")
        key = (src, page)
        if key in seen:
            continue
        seen.add(key)
        sources.append(f"{src} (page {page})")
    return sources


def generate_answer(question: str, context: str) -> str:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("user", USER_PROMPT),
        ]
    )

    messages = prompt.format_messages(context=context, question=question)

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1, 
    )

    response = llm.invoke(messages)
    return response.content


def ask(question: str, k: int = 5, use_mmr: bool = False) -> Dict[str, Any]:
    """
    End-to-end: Retrieve -> Format context -> Generate answer -> Return answer + citations.

    Returns:
      {
        "answer": str,
        "sources": [str],
        "citations": [dict],
        "num_sources": int
      }
    """
    if _looks_like_prompt_injection(question):
        return {
            "answer": "I'm sorry, I cannot process this request as it contains potentially unsafe instructions.",
            "sources": [],
            "citations": [],
            "num_sources": 0
        }

    results = retrieve_context(question, k=k, use_mmr=use_mmr)
    if not results:
        return {"answer": IDK_FALLBACK, "sources": [], "citations": [], "num_sources": 0}

    context, citations = format_retrieved_context(results)
    if not context or not citations:
        return {"answer": IDK_FALLBACK, "sources": [], "citations": [], "num_sources": 0}

    answer = generate_answer(question, context)

    sources = _build_sources_list(citations)

    if sources and answer.strip() != IDK_FALLBACK:
        answer_with_sources = answer + "\n\nSources:\n" + \
            "\n".join(f"- {s}" for s in sources)
    else:
        answer_with_sources = answer

    return {
        "answer": answer_with_sources,
        "sources": sources,
        "citations": citations,
        "num_sources": len(sources),
    }


if __name__ == "__main__":
    q = "What are the Basel III capital requirements?"
    result = ask(q, k=4, use_mmr=False)
    print(f"Question: {q}\n")
    print("Answer:\n" + result["answer"])
