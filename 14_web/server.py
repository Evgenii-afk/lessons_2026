from aiohttp import web
from hident import identify_hashes, long_solve_hash

async def define(request):
    hash_value = request.match_info['hash']
    result = identify_hashes(hash_value)
    return web.json_response(result)


async def solve(request):
    hash_value = request.query.get('hash')
    algorithm = request.query.get('algorithm')

    result = await long_solve_hash(hash_value, algorithm)
    return web.Response(text=result)


app = web.Application()

app.router.add_get('/define/{hash}', define)
app.router.add_get('/solve', solve)


web.run_app(app, host='127.0.0.1', port=8080)
