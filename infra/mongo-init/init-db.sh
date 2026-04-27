#!/bin/bash
set -e

echo "--- 🛠️ Initializing Pokedex Database ---"

# Import Pokémon
mongoimport --host localhost --db pokedex --collection pokemons \
  --type json --file /data/pokemons.json --jsonArray

# Import Moves
mongoimport --host localhost --db pokedex --collection moves \
  --type json --file /data/moves.json --jsonArray

echo "--- ✅ Import Complete! ---"