import asyncio
from tools.web_browser import fetch_content

async def researcher_agent(url: str) -> dict:
    print(f"🔎 Researching: {url}")
    content = await asyncio.to_thread(fetch_content, url)
    return {"url": url, "content": content}
