from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from analyser.schemas import EventInfo
import os
load_dotenv(override=True)
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE_NAME = os.getenv("MONGODB_DATABASE_NAME")

client = AsyncIOMotorClient(MONGODB_URI)
db = client[f"{MONGODB_DATABASE_NAME}"]
events_collection = db["events"]

async def insert_in_collection(eventinfo:dict):
    insert_response = await events_collection.insert_one(eventinfo)
    if insert_response.inserted_id:
        return {"success":True}
    return {"success":False}

async def get_all_events():
    event_list = await events_collection.find({}).to_list(length=None)
    return event_list