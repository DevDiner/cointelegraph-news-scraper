#services/mongodb_service.py

from motor.motor_asyncio import AsyncIOMotorClient
from config import config

class MongoDBService:
    def __init__(self, uri: str, db_name: str, collection_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_collection(self):
        return self.collection

    async def close(self):
        await self.client.close()

# Instantiate the MongoDB service using configuration values
db_service = MongoDBService(config.MONGO_URI, config.DB_NAME, config.MONGO_COLLECTION)
db = db_service.get_collection()
