from autogen import AssistantAgent
from autogen.tools import Tool
from my_tools.python_executor import PythonExecutorTool
from my_tools.linter import PylintTool

def get_debugger_agent(llm_config):
    executor_tool = PythonExecutorTool()
    linter_tool = PylintTool()

    system_message = (
        "You are a Python code debugger and QA expert. "
        "You can use the following tools:\n"
        "- PythonExecutor: executes python code.\n"
        "- Linter: lints python code using pylint.\n"
        "When you want to use a tool, please explicitly ask for it."
    )

    agent = AssistantAgent(
        name="Debugger",
        llm_config=llm_config,
        system_message=system_message
    )

    # Attach tools for manual use
    agent.executor_tool = executor_tool
    agent.linter_tool = linter_tool

    return agent
