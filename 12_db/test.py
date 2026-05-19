import time
from concurrent.futures import ThreadPoolExecutor
import redis  

class RedisLock:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def __enter__(self):
        while True:
            if self.redis.setnx("lock", "locked"):
                break
            time.sleep(0.01)
    
    def __exit__(self, *args):
        self.redis.delete("lock")

redis_client = redis.Redis(host='localhost', port=6379)

mu = RedisLock(redis_client)

redis_client.delete("lock")

result = 0

def function():
    with mu:  
        global result
        r = result
        time.sleep(1)
        result = r + 1

def main():  
    with ThreadPoolExecutor(max_workers=5) as executor:
        for _ in range(10):
            executor.submit(function)
    print(result)  
    
main()