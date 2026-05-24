import asyncio

import aiohttp


HASH = "c4ca4238a0b923820dcc509a6f75849b"


async def main():
    async with aiohttp.ClientSession() as session:

        async with session.get(
            f"http://localhost:8080/define/{HASH}"
        ) as response:

            data = await response.json()

        algs = data["algs"]

        print("Алгоритмы:")
        for alg in algs:
            print("-", alg)

        task_ids = []

        for alg in algs:
            async with session.get(
                "http://localhost:8080/createSolveTask",
                params={
                    "hash": HASH,
                    "algorithm": alg
                }
            ) as response:

                data = await response.json()

                task_id = data["taskId"]

                task_ids.append((alg, task_id))

        print()
        print("Ожидание результатов...")

        unfinished = set(task_ids)

        while unfinished:
            await asyncio.sleep(1)

            completed = []

            for alg, task_id in unfinished:

                async with session.get(
                    "http://localhost:8080/getPassword",
                    params={
                        "taskId": task_id
                    }
                ) as response:

                    data = await response.json()

                if "password" in data:
                    print(f"{alg}: {data['password']}")
                    completed.append((alg, task_id))

            for item in completed:
                unfinished.remove(item)


asyncio.run(main())