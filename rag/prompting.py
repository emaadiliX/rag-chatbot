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


def _looks_like_prompt_injection(text):
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


def _build_sources_list(citations):
    if not citations:
        return []

    source_pages = {}
    for c in citations:
        src = c.get("source", "Unknown")
        page = c.get("page", 1)

        if src not in source_pages:
            source_pages[src] = set()
        source_pages[src].add(page)

    sources = []
    for src, pages in source_pages.items():
        sorted_pages = sorted(pages)
        if len(sorted_pages) == 1:
            sources.append(f"{src} (page {sorted_pages[0]})")
        else:
            pages_str = ", ".join(str(p) for p in sorted_pages)
            sources.append(f"{src} (pages {pages_str})")

    return sources


def _extract_used_citation_numbers(answer):
    pattern = r'\[Source (\d+)\]'
    matches = re.findall(pattern, answer)
    return {int(n) for n in matches}


def _validate_citations(answer, num_sources):
    def replace_citation(match):
        n = int(match.group(1))
        if 1 <= n <= num_sources:
            return match.group(0)
        return ""

    pattern = r'\[Source (\d+)\]'
    return re.sub(pattern, replace_citation, answer)


def _filter_used_citations(citations, used_numbers):
    if not used_numbers:
        return []

    used_citations = []
    for num in sorted(used_numbers):
        if 1 <= num <= len(citations):
            used_citations.append(citations[num - 1])

    return used_citations


def _remove_citations_from_answer(answer):
    pattern = r'\[Source \d+\]'
    cleaned = re.sub(pattern, '', answer)
    cleaned = re.sub(r'  +', ' ', cleaned)
    cleaned = re.sub(r' ([.,;:])', r'\1', cleaned)
    return cleaned.strip()


def generate_answer(question, context):
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", USER_PROMPT),
    ])

    messages = prompt.format_messages(context=context, question=question)

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

    response = llm.invoke(messages)
    return str(response.content)


def ask(question, k=5, use_mmr=False):
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

    context, all_citations = format_retrieved_context(results)
    if not context or not all_citations:
        return {"answer": IDK_FALLBACK, "sources": [], "citations": [], "num_sources": 0}

    answer = generate_answer(question, context)

    answer = _validate_citations(answer, len(all_citations))
    used_numbers = _extract_used_citation_numbers(answer)
    used_citations = _filter_used_citations(all_citations, used_numbers)
    sources = _build_sources_list(used_citations)
    answer = _remove_citations_from_answer(answer)

    return {
        "answer": answer,
        "sources": sources,
        "citations": used_citations,
        "num_sources": len(sources),
    }


if __name__ == "__main__":
    q = "What are the Basel III capital requirements?"
    result = ask(q, k=4, use_mmr=False)
    print(f"Question: {q}\n")
    print("Answer:\n" + result["answer"])
