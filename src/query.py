import os
import sys
from typing import List, Tuple

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI

from utils import format_citation, load_settings


def build_prompt(question: str, context_blocks: List[str]) -> str:
    context = "\n\n".join(context_blocks)
    return (
        "You are a research assistant. Answer the user's question only using the provided context. "
        "If the answer is not in the context, say you do not know. "
        "Respond in the same language as the question.\n\n"
        f"Question: {question}\n\n"
        f"Context:\n{context}\n"
    )


def retrieve_context(vectorstore: Chroma, question: str, top_k: int, score_threshold: float) -> Tuple[List[str], List[str]]:
    results = vectorstore.similarity_search_with_relevance_scores(question, k=top_k)
    blocks: List[str] = []
    citations: List[str] = []
    for doc, score in results:
        if score < score_threshold:
            continue
        blocks.append(doc.page_content)
        citations.append(format_citation(doc.metadata))
    uniq_citations = list(dict.fromkeys(citations))
    return blocks, uniq_citations


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python src/query.py \"your question\"")
        return

    question = sys.argv[1]
    settings = load_settings(os.path.join("configs", "settings.yaml"))

    embeddings = HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": settings.embedding_device},
    )
    vectorstore = Chroma(
        persist_directory=settings.chroma_dir,
        collection_name=settings.collection_name,
        embedding_function=embeddings,
    )

    blocks, citations = retrieve_context(
        vectorstore,
        question,
        settings.top_k,
        settings.score_threshold,
    )

    if not blocks:
        print("No relevant context found. Try a different question or lower score_threshold.")
        return

    api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        print("DEEPSEEK_API_KEY is not set.")
        return

    llm = ChatOpenAI(
        base_url=settings.deepseek_base_url,
        model=settings.deepseek_model,
        temperature=settings.temperature,
        api_key=api_key,
    )

    prompt = build_prompt(question, blocks)
    response = llm.invoke(prompt)

    print(response.content)
    print("\nCitations:")
    for cite in citations:
        print(f"- {cite}")


if __name__ == "__main__":
    main()
