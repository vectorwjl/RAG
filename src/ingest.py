import os

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils import extract_documents_from_pdf, get_pdf_paths, load_settings


def main() -> None:
    settings = load_settings(os.path.join("configs", "settings.yaml"))
    pdf_paths = get_pdf_paths(settings.data_dir)
    if not pdf_paths:
        print(f"No PDF files found in {settings.data_dir}")
        return

    all_docs = []
    for pdf_path in pdf_paths:
        docs = extract_documents_from_pdf(pdf_path)
        all_docs.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    split_docs = splitter.split_documents(all_docs)

    embeddings = HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": settings.embedding_device},
    )

    os.makedirs(settings.chroma_dir, exist_ok=True)
    vectorstore = Chroma.from_documents(
        split_docs,
        embeddings,
        persist_directory=settings.chroma_dir,
        collection_name=settings.collection_name,
    )
    vectorstore.persist()

    print(f"Ingested {len(split_docs)} chunks from {len(pdf_paths)} PDFs")


if __name__ == "__main__":
    main()
