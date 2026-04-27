from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class MongoManager:
    def __init__(self):
        uri = os.getenv("MONGO_URL")
        self.client = MongoClient(uri)
        self.db = self.client["pokedex"]
        
    @property
    def pokemons(self):
        return self.db["pokemons"]

    @property
    def moves(self):
        return self.db["moves"]

# Singleton instance
db_manager = MongoManager()