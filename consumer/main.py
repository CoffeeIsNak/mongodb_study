# consumer/main.py

import asyncio
from writer import LogConsumer

async def main():
    consumer = LogConsumer()
    await consumer.run()

if __name__ == "__main__":
    asyncio.run(main())
