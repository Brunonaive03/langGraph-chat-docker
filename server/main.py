from server.core.app import mcp
from server.core.logs import logger
import server.tools # This triggers the tool registration

if __name__ == "__main__":
    logger.info("Starting Pokedex Server...")
    mcp.run()