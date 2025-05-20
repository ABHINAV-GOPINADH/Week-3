# agents/coder.py

from autogen import AssistantAgent

def get_coder_agent(llm_config):
    return AssistantAgent(
        name="Coder",
        llm_config=llm_config,
        system_message=(
            "You are a helpful Python coding assistant. "
            "Your job is to write clean, functional Python code. "
            "Collaborate with the Debugger to refine and fix code issues. "
            "Only produce code that can be executed and tested. "
            "Ensure function names and indentation are correct."
        )
    )
