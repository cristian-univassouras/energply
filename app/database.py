from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://mongodb:27017"

client = AsyncIOMotorClient(MONGO_URL)
database = client.enegiply
collection = database.leituras

