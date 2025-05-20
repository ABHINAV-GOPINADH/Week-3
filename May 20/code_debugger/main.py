import asyncio
from autogen import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager
from my_tools.python_executor import PythonExecutorTool
from my_tools.linter import PylintTool
from config.gemini_config import get_gemini_llm_config
from agents.coder import get_coder_agent
from agents.debugger import get_debugger_agent

# Load LLM config
llm_config = get_gemini_llm_config()

# Initialize tools
executor_tool = PythonExecutorTool()
linter_tool = PylintTool()

# Agents
coder = get_coder_agent(llm_config)
debugger = get_debugger_agent(llm_config)

# User-facing agent
user_proxy = UserProxyAgent(
    name="User",
    code_execution_config={"use_docker": False}
)

# Group Chat setup
groupchat = GroupChat(
    agents=[user_proxy, coder, debugger],
    messages=[],
    max_round=10,
    speaker_selection_method="round_robin",
)

manager = GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config
)

async def run_debugger():
    await user_proxy.a_initiate_chat(manager, message="""
Hi! Please write a Python function that checks if a number is prime. Then debug it.
""")

if __name__ == "__main__":
    asyncio.run(run_debugger())
