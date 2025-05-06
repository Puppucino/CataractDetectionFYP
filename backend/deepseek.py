from fastapi import APIRouter, HTTPException, Request
import os
import requests
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

@router.post("/explain")
async def explain_result(request: Request):
    data = await request.json()
    last_name = data.get("lastName", "Patient")
    # If chat history is provided, use it for context
    if "messages" in data:
        messages = data["messages"]
        prompt = f"You are an AI ophthalmologist. Address the user as Mr./Ms. {last_name}. Continue the conversation and reply in short, clear paragraphs or bullet points."
        messages = [{"role": m["role"], "content": m["content"]} for m in messages]
        messages.insert(0, {"role": "system", "content": prompt})
    else:
        result = data.get("result", "")
        prompt = f"You are an AI ophthalmologist. Address the user as Mr./Ms. {last_name}. Explain what this result means for the patient: {result}. Reply in short, clear paragraphs or bullet points."
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": result}
        ]
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            json={
                "model": "deepseek-chat",
                "messages": messages,
                "temperature": 1.3
            },
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }
        )
        response.raise_for_status()
        explanation = response.json()["choices"][0]["message"]["content"]
        return {"explanation": explanation}
    except Exception as err:
        print("DeepSeek API error:", err)
        raise HTTPException(status_code=500, detail="Failed to get explanation") 