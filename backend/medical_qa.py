from fastapi import APIRouter, HTTPException, Request
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
import os
import requests
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

INDEX_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'medical_vectorstore'))
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Load vectorstore and set up retriever
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()

@router.post("/qa")
async def medical_qa(request: Request):
    data = await request.json()
    question = data.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="Missing question")
    # Retrieve relevant documents
    docs = retriever.get_relevant_documents(question)
    context = "\n".join([doc.page_content for doc in docs])
    prompt = f"You are a helpful medical assistant. Use the following context to answer the user's question.\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"
    messages = [
        {"role": "system", "content": "You are a helpful medical assistant. Answer with citations if possible."},
        {"role": "user", "content": prompt}
    ]
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            json={
                "model": "deepseek-chat",
                "messages": messages,
                "temperature": 0.2
            },
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }
        )
        response.raise_for_status()
        answer = response.json()["choices"][0]["message"]["content"]
    except Exception as err:
        print("DeepSeek API error:", err)
        raise HTTPException(status_code=500, detail="Failed to get answer from DeepSeek")
    sources = [doc.metadata.get("source", "") for doc in docs]
    return {"answer": answer, "sources": sources} 