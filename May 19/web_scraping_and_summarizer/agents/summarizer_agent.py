from tools.text_summarizer import summarize_text

async def summarizer_agent(research: dict) -> str:
    print(f"🧠 Summarizing content from: {research['url']}")
    summary = await summarize_text(research["content"])
    return summary
