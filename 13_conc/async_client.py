import asyncio
import aiohttp

async def fetch(session, i, semaphore):
    async with semaphore:  
        async with session.get(f'http://localhost:8003/{i}') as response:
            data = await response.json()
            return data['data']

async def async_requests(count=100_000, concurrency=100):
    semaphore = asyncio.Semaphore(concurrency)
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, i, semaphore) for i in range(count)]
        results = await asyncio.gather(*tasks)
    
    return results

if __name__ == "__main__":
    asyncio.run(async_requests(count=1000, concurrency=50))