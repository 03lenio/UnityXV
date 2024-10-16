import time

import pymongo

from ..memories.memory import Memory
from pymongo import MongoClient


class DatabaseManager:

    def __init__(self):
        self.mongo_client = MongoClient('localhost', 27017)
        self.db = self.mongo_client["UnityXV"]
        self.memories = self.db["memories"]
        self.contexts = self.db["contexts"]

    def save_memory_to_db(self, memory: Memory):
        self.memories.insert_one({"timestamp": memory.get_timestamp(), "memory": memory.get_memory()})

    def get_memories_from_db(self, count: int):
        return self.memories.find().sort("timestamp", pymongo.DESCENDING).limit(count)

    def get_memories_from_db_str(self, count: int):
        last_memories = self.memories.find().sort("timestamp", pymongo.DESCENDING).limit(count)
        to_return = []
        for memory in last_memories:
            to_return.append(memory.get("memory"))
        return to_return

    def save_context_to_db(self, context: str):
        self.contexts.insert_one({"timestamp": time.time(), "context": context, "obsolete": False})

    def get_context_from_db(self, count: int):
        return self.contexts.find({"obsolete": False}).sort("timestamp", pymongo.DESCENDING).limit(count)

    def mark_context_obsolete(self, timestamp):
        self.contexts.update_one({"timestamp": timestamp}, {"$set": {"obsolete": True}})

    def get_non_obsolete_context_count(self):
        return len(self.contexts.find({"obsolete": False}).to_list())


