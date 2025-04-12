# consumer/bulk_updater.py

import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import UpdateOne
from faker import Faker
import random


class AsyncBulkUpdater:
    def __init__(self, mongo_url="mongodb://mongo:27017", db_name="log_db", collection_name="user_logs"):
        self.mongo_url = mongo_url
        self.db_name = db_name
        self.collection_name = collection_name
        self.mongo = None
        self.collection = None
        self.fake = Faker()

    async def connect(self):
        self.mongo = AsyncIOMotorClient(self.mongo_url)
        self.collection = self.mongo[self.db_name][self.collection_name]

    def generate_fake_docs(self, count):
        """Update 대상이 될 기존 문서들을 만드는 용도."""
        return [
            {
                "user_id": f"user_{i}",
                "action": random.choice(["click", "view_item", "checkout", "buy_item", "add_to_cart"]),
                "score": random.randint(1, 5)
            }
            for i in range(count)
        ]

    async def insert_seed_data(self, docs):
        await self.collection.insert_many(docs)
        print(f"[Seed Insert] {len(docs)}개 문서 삽입 완료")

    async def bulk_update(self, count):
        """수정할 문서 수만큼 bulk update 수행"""
        ops = [
            UpdateOne({"user_id": f"user_{i}"}, {"$set": {"action": "reviewed"}}, upsert=True)
            for i in range(count)
        ]

        start = datetime.datetime.now()
        result = await self.collection.bulk_write(ops, ordered=False)
        end = datetime.datetime.now()

        duration = (end - start).total_seconds()
        print(f"✅ {count} documents bulk update completed")
        print(f"⏱ duration: {duration:.3f} seconds")
        return duration
