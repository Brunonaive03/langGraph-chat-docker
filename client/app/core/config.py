import warnings
import logging

def setup_environment():
    """Configures warnings and logging suppressions for all providers."""
    # Mute the schema warnings for Gemini
    warnings.filterwarnings("ignore", message=".*additionalProperties.*")
    
    # Suppress internal library noise
    logging.getLogger("mcp").setLevel(logging.ERROR)
    logging.getLogger("langchain_google_genai").setLevel(logging.ERROR)
    logging.getLogger("langchain_ollama").setLevel(logging.ERROR)
    
    # Reduce HTTP noise from local Ollama or Cloud API calls
    logging.getLogger("httpx").setLevel(logging.WARNING)