import asyncio
from agents.researcher_agent import researcher_agent
from agents.summarizer_agent import summarizer_agent

async def web_research_assistant(url: str):
    print("🚀 Web Research Assistant Started")

    # Step 1: Research
    research_data = await researcher_agent(url)

    # Step 2: Summarize
    summary = await summarizer_agent(research_data)

    print("\n✅ Final Summary:\n")
    print(summary)

if __name__ == "__main__":
    # Example URL to research
    url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    asyncio.run(web_research_assistant(url))
