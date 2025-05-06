from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import os

ARTICLES_DIR = "medical_articles"
INDEX_DIR = "medical_vectorstore"

# Load all articles
docs = []
for fname in os.listdir(ARTICLES_DIR):
    if fname.endswith(".txt"):
        with open(os.path.join(ARTICLES_DIR, fname), encoding="utf-8") as f:
            text = f.read()
            docs.append(text)

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
all_chunks = []
for doc in docs:
    all_chunks.extend(splitter.split_text(doc))

# Create embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Build vectorstore
vectorstore = FAISS.from_texts(all_chunks, embeddings)
vectorstore.save_local(INDEX_DIR)

print(f"Indexed {len(all_chunks)} chunks from {len(docs)} articles. Vectorstore saved to {INDEX_DIR}/") 