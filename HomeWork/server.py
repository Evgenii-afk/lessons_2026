import asyncio

from aiohttp import web

from hident import identify_hashes, long_solve_hash


tasks = {}
task_counter = 0


async def define(request):
    input_hash = request.match_info["hash"]

    algs = identify_hashes(input_hash)

    return web.json_response({
        "algs": algs
    })


async def create_solve_task(request):
    global task_counter

    input_hash = request.query["hash"]
    algorithm = request.query["algorithm"]

    task_counter += 1
    task_id = task_counter

    task = asyncio.create_task(
        long_solve_hash(input_hash, algorithm)
    )

    tasks[task_id] = task

    return web.json_response({
        "taskId": task_id
    })


async def get_password(request):
    task_id = int(request.query["taskId"])

    task = tasks.get(task_id)

    if task is None:
        return web.json_response({
            "err": {
                "code": 1000,
                "message": "task not found"
            }
        })

    if not task.done():
        return web.json_response({
            "err": {
                "code": 1001,
                "message": "task not finished"
            }
        })

    password = task.result()

    return web.json_response({
        "password": password
    })


app = web.Application()

app.router.add_get("/define/{hash}", define)
app.router.add_get("/createSolveTask", create_solve_task)
app.router.add_get("/getPassword", get_password)

web.run_app(app, port=8080)