from src.helper import repo_repsitry, load_repo, chunk_split, load_embedding
import faiss
from langchain.vectorstores import FAISS

# Load documents from local repo folder
documents = load_repo("repo/")
texts = chunk_split(documents)
embeddings = load_embedding()

# Create and save FAISS vector database
vectordb = FAISS.from_documents(texts, embeddings)
vectordb.save_local("research/faiss_index")