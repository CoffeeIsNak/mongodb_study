from faker import Faker
import random, asyncio, json
import redis.asyncio as aioredis

class LogProducer:
    def __init__(self, queue_url="redis://redis:6379"):
        self.fake = Faker()
        self.actions = ["click", "view_item", "checkout", "buy_item", "add_to_cart"]
        self.redis = None
        self.queue_url = queue_url

    def generate_log(self):
        while True:
            yield {
                "user_id": self.fake.user_name(),
                "action": random.choice(self.actions),
                "item_id": f"item_{random.randint(1,100)}",
                "timestamp": self.fake.date_time_this_year().isoformat()
            }

    async def connect(self):
        self.redis = await aioredis.from_url(self.queue_url)

    async def run(self, interval=0.5):
        await self.connect()
        for log in self.generate_log():
            await self.redis.rpush("logs", json.dumps(log))
            print(f"[Producer] {log} rpushed to redis!!")
            await asyncio.sleep(interval)  # Async로 비동기 간격 조절
