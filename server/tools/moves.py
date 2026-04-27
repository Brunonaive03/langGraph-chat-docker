from server.core.app import mcp
from server.core.db import db_manager

@mcp.tool()
def fetch_move_data(name: str) -> str:
    """Get power, accuracy, and category for a specific move."""
    move = db_manager.moves.find_one({"name": name.upper()})
    if move:
        move.pop("_id", None)
        return str(move)
    return f"Move '{name}' not found."