import os


def get_gemini_llm_config():
    return {
        "model": "gemini-2.0-flash",
        "api_key":os.getenv("GEMINI_API_KEY"),
        "temperature": 0.7,
        "api_type": "google",
    }
