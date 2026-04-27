import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

def get_model():
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    if provider == "ollama_cloud":
        return ChatOpenAI(
            model=os.getenv("OLLAMA_CLOUD_MODEL", "qwen3-coder:480b-cloud"),
            openai_api_base=os.getenv("OLLAMA_CLOUD_BASE_URL", "https://ollama.com/v1"),
            openai_api_key=os.getenv("OLLAMA_CLOUD_API_KEY"),
            temperature=0,
        )
    else:
        return ChatGoogleGenerativeAI(
            model=os.getenv("GOOGLE_MODEL", "gemini-3-flash-preview"),
            temperature=0,
        )