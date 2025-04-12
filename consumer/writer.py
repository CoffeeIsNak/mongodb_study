# consumer/writer.py

import json
import asyncio
import redis.asyncio as aioredis
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime


class LogConsumer:
    def __init__(self, redis_url="redis://redis:6379", mongo_url="mongodb://mongo:27017"):
        self.redis_url = redis_url
        self.mongo_url = mongo_url
        self.queue_key = "logs"
        self.redis = None
        self.mongo = None
        self.collection = None

    async def connect(self):
        self.redis = await aioredis.from_url(self.redis_url)
        self.mongo = AsyncIOMotorClient(self.mongo_url)
        self.collection = self.mongo["log_db"]["user_logs"]

    async def log_stream(self):
        """Generator-like async iterator that yields logs from Redis."""
        while True:
            log = await self.redis.lpop(self.queue_key)
            if log:
                yield json.loads(log)
            else:
                await asyncio.sleep(0.5)  # 잠깐 쉬면서 기다림

    async def run(self):
        await self.connect()
        async for log in self.log_stream():
            log['timestamp'] = datetime.fromisoformat(log['timestamp'])
            await self.collection.insert_one(log)
            print(f"[Mongo Inserted] {log} into collection: {self.collection}")
