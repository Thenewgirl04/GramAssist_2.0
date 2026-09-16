import json
from pathlib import Path
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"


def load_chunks(file_path):
    data = json.loads(Path(file_path).read_text())

    documents = [
        Document(
            page_content=chunk["content"],
            metadata=chunk["metadata"]
        )
        for chunk in data["chunks"]
    ]

    return documents

def create_faiss_index(chunks, faiss_dir):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(faiss_dir)
    print(f"[+] Saved FAISS index to {faiss_dir}")


def load_faiss_index(faiss_dir):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore= FAISS.load_local(faiss_dir, embeddings, allow_dangerous_deserialization=True)
    return vectorstore

def create_retriever(faiss_dir):
    vectorstore = load_faiss_index(faiss_dir)
    retriever = vectorstore.as_retriever(search_kwargs={"k":3})
    return retriever

def retrieval_pipeline():
    recursive_chunks = load_chunks(RESULTS_DIR / "heading_recursive_2500_250.json")
    semantic_chunks = load_chunks(RESULTS_DIR / "heading_hybrid_chunking.json")
    create_faiss_index(
        recursive_chunks,
        "faiss/heading_recursive"
    )

    create_faiss_index(
        semantic_chunks,
        "faiss/heading_semantic"
    )

def test_retrieval(faiss_dir, question, k=3):
    vectorstore = load_faiss_index(faiss_dir)

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": k}
    )

    documents = retriever.invoke(question)

    print(f"\nQUESTION: {question}")

    for i, doc in enumerate(documents, start=1):
        print(f"\n{'=' * 70}")
        print(f"RESULT {i}")
        print("Metadata:", doc.metadata)
        print("-" * 70)
        print(doc.page_content)

    return documents


if __name__ == "__main__":
    retrieval_pipeline()