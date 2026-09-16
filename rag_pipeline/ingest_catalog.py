from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from project_paths import CATALOG_INDEX_PATH, CATALOG_MARKDOWN_PATH

class CatalogIngestor:
    def __init__(self, input_path:Path, faiss_path: Path):
        self.input_path = input_path
        self.headers_to_split = [
                    ("#", "Header 1"),
                    ("##", "Header 2"),
                    ("###", "Header 3"),
                    ("####", "Header 4"),
                ]
        self.faiss_path = faiss_path

    def load_catalog(self):
        return self.input_path.read_text(encoding="utf-8")

    def split_by_headers(self, markdown):
        markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=self.headers_to_split,
        strip_headers=False)

        return markdown_splitter.split_text(markdown)

    def split_sections(self, sections):
        section_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2500,
            chunk_overlap=250
        )
        return section_splitter.split_documents(sections)

    def split_catalog(self):
        header_split = self.split_by_headers(self.load_catalog())
        section_split = self.split_sections(header_split)

        return section_split

    def create_embeddings(self):
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def create_faiss_index(self):
        vectorstore = FAISS.from_documents(self.split_catalog(), self.create_embeddings())
        vectorstore.save_local(self.faiss_path)
        print(f"[+] Saved FAISS index to {self.faiss_path}")


if __name__ == "__main__":
    ingestor = CatalogIngestor(
        input_path=CATALOG_MARKDOWN_PATH,
        faiss_path=CATALOG_INDEX_PATH,
    )

    ingestor.create_faiss_index()
