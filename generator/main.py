# generator/main.py
import asyncio
from producer import LogProducer

async def main():
    producer = LogProducer()
    await producer.run()

asyncio.run(main())
