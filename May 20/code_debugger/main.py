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
    code_execution_config={"use_docker": False},
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

# File paths
BUGGY_FILE_PATH = "buggy_code.py"
FIXED_FILE_PATH = "buggy_code.py"  # Overwriting same file

async def run_debugger():
    # Step 1: Read the buggy code
    with open(BUGGY_FILE_PATH, "r") as file:
        buggy_code = file.read()

    # Step 2: Construct the prompt
    prompt = f"""Please fix the following Python code and provide the corrected code only (no explanation):

```python
{buggy_code}
```"""

    # Step 3: Run the group chat and capture the final message
    await user_proxy.a_initiate_chat(manager, message=prompt)

    # Step 4: Get last message from the groupchat to extract the final fixed code
    last_msg = groupchat.messages[-1].content

    # Step 5: Extract only the corrected code (assuming it’s inside a markdown code block)
    if "```python" in last_msg:
        corrected_code = last_msg.split("```python")[1].split("```")[0].strip()
    else:
        corrected_code = last_msg.strip()

    # Step 6: Write corrected code back to file
    with open(FIXED_FILE_PATH, "w") as file:
        file.write(corrected_code)

if __name__ == "__main__":
    asyncio.run(run_debugger())
