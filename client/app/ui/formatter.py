from langchain_core.messages import AIMessage

# ANSI Color Codes
BLUE = "\033[94m"
GREEN = "\033[92m"
GRAY = "\033[90m"
RESET = "\033[0m"
BOLD = "\033[1m"

def format_content(content) -> str:
    """Handles both string content and Gemini's list-of-dicts format."""
    if isinstance(content, list):
        # Extract text from multimodal/metadata blocks
        parts = [part['text'] for part in content if isinstance(part, dict) and 'text' in part]
        return " ".join(parts).strip()
    return str(content).strip()

def print_assistant(message: AIMessage):
    """Prints the AI response in Blue."""
    text = format_content(message.content)
    if text:
        print(f"\n{BLUE}{BOLD}Assistant:{RESET} {text}")

def print_user_prompt():
    """Returns the formatted prompt string for input()."""
    return f"\n{GREEN}{BOLD}You:{RESET} "

def print_system_log(text: str):
    """Prints background actions (like tool calls) in Gray."""
    print(f"{GRAY}[{text}]{RESET}")

def print_tools_status(tools):
    """Prints the list of loaded MCP tools."""
    names = [t.name for t in tools]
    print(f"{GRAY}MCP tools loaded: {names}{RESET}")

def print_header():
    """Initial app branding."""
    print(f"\n{BLUE}{'='*40}")
    print(f"{BOLD}   POKEDEX CLI - MODULAR VERSION")
    print(f"{'='*40}{RESET}")

def print_shutdown():
    """Clean exit message."""
    print(f"\n{GRAY}[Shutdown signal received. Closing Pokedex connection...]{RESET}")

def print_exit_message():
    """Final session exit message."""
    print(f"\n{GRAY}[Session Closed]{RESET}")
    print("Goodbye!")