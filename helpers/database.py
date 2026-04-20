from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(Config.MONGO_URI)
        self.db = self.client["stream_editor"]
        self.users = self.db["users"]
        self.settings = self.db["settings"]

    async def add_user(self, user_id):
        if not await self.users.find_one({"id": user_id}):
            await self.users.insert_one({"id": user_id, "banned": False})

    async def get_total_users(self):
        return await self.users.count_documents({})

    async def is_banned(self, user_id):
        user = await self.users.find_one({"id": user_id})
        return user.get("banned", False) if user else False

    async def ban_user(self, user_id):
        await self.users.update_one({"id": user_id}, {"$set": {"banned": True}})

    async def unban_user(self, user_id):
        await self.users.update_one({"id": user_id}, {"$set": {"banned": False}})

    async def get_all_users(self):
        return self.users.find({})

db = Database()
