from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from functools import lru_cache
from project_paths import CATALOG_INDEX_PATH

class CatalogRetriever:
    def __init__(self, faiss_path):
        self.faiss_path = faiss_path

    def load_faiss_index(self):
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        vectorstore = FAISS.load_local(self.faiss_path, embeddings, allow_dangerous_deserialization=True)
        return vectorstore

    def create_retriever(self):
        vectorstore = self.load_faiss_index()
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        return retriever


@lru_cache(maxsize=1)
def get_catalog_retriever():
    catalog = CatalogRetriever(
        faiss_path=CATALOG_INDEX_PATH
    )

    return catalog.create_retriever()

def retrieve_similar_chunks(question):
    retriever = get_catalog_retriever()
    documents = retriever.invoke(question)
    return documents
