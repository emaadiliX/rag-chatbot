import re
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
3. Cite sources using [Source N] markers where N corresponds to the source numbers in the context above.
4. Only use the "I don't have enough information..." fallback if the documents provide no information at all about the entities or topics in the question.

Answer:
"""


def is_prompt_injection(text):
    """Check if the text contains common prompt injection patterns."""
    if not text:
        return False

    patterns = [
        r"ignore (all|any|previous) instructions",
        r"system prompt",
        r"reveal.*(prompt|instructions)",
        r"override",
        r"forget your",
        r"new instructions",
        r"disregard",
    ]
    return any(re.search(p, text, flags=re.IGNORECASE) for p in patterns)


def process_citations(answer, all_citations):
    """
    Extract which sources the LLM actually used, build a clean sources list,
    and remove citation markers from the answer text.
    """
    used_nums = {int(n) for n in re.findall(r'\[Source (\d+)\]', answer)}

    used_citations = [
        all_citations[n - 1] for n in sorted(used_nums)
        if 1 <= n <= len(all_citations)
    ]

    source_pages = {}
    for c in used_citations:
        src = c.get("source", "Unknown")
        page = c.get("page", 1)
        if src not in source_pages:
            source_pages[src] = set()
        source_pages[src].add(page)

    sources = []
    for src, pages in source_pages.items():
        pages_sorted = sorted(pages)
        if len(pages_sorted) == 1:
            sources.append(f"{src} (page {pages_sorted[0]})")
        else:
            sources.append(
                f"{src} (pages {', '.join(map(str, pages_sorted))})")

    clean_answer = re.sub(r'\[Source \d+\]', '', answer)
    # collapse multiple spaces
    clean_answer = re.sub(r'  +', ' ', clean_answer)
    # fix spacing before punctuation
    clean_answer = re.sub(r' ([.,;:])', r'\1', clean_answer)

    return clean_answer.strip(), sources, used_citations


def generate_answer(question, context):
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", USER_PROMPT),
    ])

    messages = prompt.format_messages(context=context, question=question)

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

    response = llm.invoke(messages)
    return str(response.content)


def ask(question, k=5):
    if is_prompt_injection(question):
        return {
            "answer": "I'm sorry, I cannot process this request.",
            "sources": [],
            "citations": [],
            "num_sources": 0
        }

    results = retrieve_context(question, k=k)
    if not results:
        return {"answer": IDK_FALLBACK, "sources": [], "citations": [], "num_sources": 0}

    context, all_citations = format_retrieved_context(results)
    if not context:
        return {"answer": IDK_FALLBACK, "sources": [], "citations": [], "num_sources": 0}

    answer = generate_answer(question, context)
    answer, sources, used_citations = process_citations(answer, all_citations)

    return {
        "answer": answer,
        "sources": sources,
        "citations": used_citations,
        "num_sources": len(sources),
    }


if __name__ == "__main__":
    q = "What are the Basel III capital requirements?"
    result = ask(q, k=4)
    print(f"Question: {q}\n")
    print("Answer:\n" + result["answer"])
