import asyncio
import pandas as pd
import matplotlib.pyplot as plt
import aiofiles
from autogen import GroupChat, GroupChatManager, UserProxyAgent, AssistantAgent
import google.generativeai as genai

# Set up Gemini
config_list = [
    {
        "model": "gemini-1.5-flash",
        "api_key": "AIzaSyAtY7Pm8uXIYQez_Bt251_zYQg3OORsm2A",  # Replace with your actual API key
        "api_type": "google",
    }
]

llm_config = {
    "seed": 42,
    "temperature": 0,
    "config_list": config_list,
}

# Tool: Visualize Data
async def visualize_data(df, column, chart_type='hist', output='output.png'):
    plt.figure(figsize=(10, 6))
    if chart_type == 'hist':
        df[column].hist()
    elif chart_type == 'bar':
        df[column].value_counts().plot(kind='bar')
    elif chart_type == 'line':
        df[column].plot(kind='line')
    plt.title(f'{chart_type.title()} of {column}')
    plt.savefig(output)
    plt.close()
    return output


data_fetcher = AssistantAgent(
    name="DataFetcher",
    llm_config=llm_config,
    system_message="""
        You are a data-fetching assistant. Your job is to:
        1. Load the CSV file using pandas.
        2. Print the first few rows.
        3. Describe the columns, types, and missing values.
        4. Share a summary of the structure with the Analyst agent.
        Ensure your output is clear and concise for downstream use.
        """,
    code_execution_config={"use_docker": False}  # ✅ Required here too
)

analyst = AssistantAgent(
    name="Analyst",
    llm_config=llm_config,
    system_message="""
        You are a data analyst. Once the dataset is shared by the DataFetcher:
        1. Perform basic descriptive statistics (mean, median, mode, std).
        2. Generate appropriate visualizations (histograms, scatter plots, box plots, etc.).
        3. Draw insights or trends where possible.

        Make sure the code you generate is valid and save plots with meaningful names.
        """,
    code_execution_config={"use_docker": False}  # ✅ Required here too
)

# User Proxy (initiates the task)
user_proxy = UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    code_execution_config={
        "use_docker": False  # ✅ This disables Docker and uses local Python
    }
)

# GroupChat with RoundRobin strategy
group_chat = GroupChat(
    agents=[user_proxy, data_fetcher, analyst],
    messages=[],
    max_round=10,
    speaker_selection_method="round_robin",
)
chat_manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)

# Async execution function
async def run_analysis_pipeline(csv_path):
    await user_proxy.a_initiate_chat(
        chat_manager,
        message=f"""
        Let's begin the data analysis pipeline.
        Please load the CSV from this path: {csv_path}.
        Then analyze the data, suggest some visualizations,
        and generate at least one chart for a column with numerical data.
        Finally, say TERMINATE when done.
        """
    )

# Run main loop
if __name__ == "__main__":
    csv_file_path = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"  # Sample dataset
    asyncio.run(run_analysis_pipeline(csv_file_path))