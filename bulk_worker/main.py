# consumer/main.py

import asyncio
from bulk_updater import AsyncBulkUpdater

async def main():
    updater = AsyncBulkUpdater(db_name="bulk_benchmark_db", collection_name="test_set")

    await updater.connect()

    # 실험할 문서 수
    sizes = [100, 200, 500, 1000, 1500, 2000, 5000]

    for count in sizes:
        # 1. 문서 생성 & 적재
        seed_docs = updater.generate_fake_docs(count)
        await updater.insert_seed_data(seed_docs)

        # 2. bulk update 수행 & 시간 측정
        await updater.bulk_update(count)

        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())
