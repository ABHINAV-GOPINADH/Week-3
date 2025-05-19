import google.generativeai as genai
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

async def summarize_text(text: str) -> str:
    prompt = f"Summarize the following content in concise, clear language:\n\n{text}"
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text.strip()
