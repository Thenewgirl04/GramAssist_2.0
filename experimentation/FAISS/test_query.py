"""
We tested whether semantic chunking improved retrieval over a simpler structure-aware recursive strategy.
It didn't meaningfully improve retrieval on this document because the catalog's heading structure already provides strong semantic boundaries.
Final choice: MarkdownHeaderTextSplitter → RecursiveCharacterTextSplitter(2500, 250)
"""

from indexer import load_faiss_index
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

RECURSIVE_INDEX = BASE_DIR / "faiss" / "heading_recursive"
SEMANTIC_INDEX = BASE_DIR / "faiss" / "heading_semantic"

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

def compare_retrieval(question):
    print("\n" + "#" * 80)
    print("HEADING + RECURSIVE")
    print("#" * 80)

    test_retrieval(RECURSIVE_INDEX,
        question
    )

    print("\n" + "#" * 80)
    print("HEADING + SEMANTIC")
    print("#" * 80)

    test_retrieval(
        SEMANTIC_INDEX,
        question
    )
questions = [
    "If I retake a class, does my old grade still affect my GPA?",
    "Do all of my transfer classes count toward my degree?",
    "Can I leave a class after the withdrawal deadline?",
    "I'm transferring in with 35 credits. Do I still have to take FYE?",
    "Can a senior take a graduate-level course?",
]

if __name__ == "__main__":
    for question in questions:
        compare_retrieval(
        question
        )

