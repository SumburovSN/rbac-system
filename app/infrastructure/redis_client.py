import redis.asyncio as redis

async def get_redis_client():
    client = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True,
    )
    try:
        yield client
    finally:
        await client.aclose()
