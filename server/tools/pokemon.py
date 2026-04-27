from server.core.app import mcp
from server.core.db import db_manager

@mcp.tool()
def fetch_pokemon_data(name: str) -> str:
    """Get full stats, types, and moves for a specific Pokemon."""
    pokemon = db_manager.pokemons.find_one({"name": name.upper()})
    if pokemon:
        pokemon.pop("_id", None)
        return str(pokemon)
    return f"Pokemon '{name}' not found."

@mcp.tool()
def search_by_type(type_code: str) -> str:
    """Find all Pokemon of a specific type (e.g. GRS, FIRE)."""
    cursor = db_manager.pokemons.find({"type": type_code.upper()})
    names = [p["name"] for p in cursor]
    return f"Found: {', '.join(names)}" if names else "No matches."

@mcp.tool()
def check_evolution(name: str) -> str:
    """Check what a Pokemon evolves from and how."""
    pokemon = db_manager.pokemons.find_one({"name": name.upper()}, {"name": 1, "evolution": 1})
    if not pokemon: return "Not found."
    
    ev = pokemon.get("evolution")
    if not ev or not ev.get("from"):
        return f"{name} does not evolve from anything."
    return f"{name} evolves from {ev['from']} via {ev['method']}."