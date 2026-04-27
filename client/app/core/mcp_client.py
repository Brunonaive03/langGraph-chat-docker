import os
from pathlib import Path
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp import ClientSession
from langchain_mcp_adapters.tools import load_mcp_tools

base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
server_path = os.path.join(base_path, "server", "main.py")

class PokedexMCPClient:
    def __init__(self):
        # 1. Get the project root (langGraph-chat)
        # This assumes mcp.py is in client/app/core/
        root_path = Path(__file__).parent.parent.parent.parent.absolute()
        
        self.server_params = StdioServerParameters(
            command="python3",
            args=["-m", "server.main"],
            # Explicitly set the working directory to the project root
            cwd=str(root_path),
            env={**os.environ, "PYTHONPATH": str(root_path)},
        )

    def get_context(self):
        """Returns the async context managers for the stdio connection."""
        return stdio_client(self.server_params)

    async def fetch_tools(self, session: ClientSession):
        """Wraps the adapter call."""
        return await load_mcp_tools(session)