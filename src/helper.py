import os
from git import Repo
from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

# Clone any GitHub repository
import shutil

def repo_repsitry(repo_url):
    repo_path = "repo/"

    # Check if repo folder exists and contains .py files
    if os.path.exists(repo_path) and any(file.endswith(".py") for root, dirs, files in os.walk(repo_path) for file in files):
        print("[INFO] Repository already exists and contains .py files. Skipping cloning.")
        return  

    # Else: delete old folder if it exists and clone new one
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    os.makedirs(repo_path, exist_ok=True)
    print("[INFO] Cloning repository...")
    Repo.clone_from(repo_url, to_path=repo_path)
    print("[INFO] Repository cloned successfully.")


# Load .py files from repo
def load_repo(repo_path):
    loader = GenericLoader.from_filesystem(
        repo_path,
        glob="**/*",
        suffixes=[".py"],
        parser=LanguageParser(language=Language.PYTHON, parser_threshold=500)
    )
    documents = loader.load()
    return documents

# Split documents into chunks
def chunk_split(documents):
    text_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,
        chunk_size=300,
        chunk_overlap=20
    )
    texts = text_splitter.split_documents(documents)
    return texts

# Load embedding model
def load_embedding():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings