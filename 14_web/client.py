import aiohttp
import asyncio

HASH = "c4ca4238a0b923820dcc509a6f75849b"


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://127.0.0.1:8080/define/{HASH}') as resp:
            algorithms = await resp.json()
            print("Алгоритмы:", algorithms)

        for alg in algorithms:
            async with session.get(
                f'http://127.0.0.1:8080/solve?hash={HASH}&algorithm={alg}'
            ) as resp:
                result = await resp.text()
                print(f"{alg} -> {result}")


asyncio.run(main())