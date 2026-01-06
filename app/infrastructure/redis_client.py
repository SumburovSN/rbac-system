import redis.asyncio as redis
from app.config import REDIS_HOST, REDIS_PORT

async def get_redis_client():
    client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        decode_responses=True,
    )
    try:
        yield client
    finally:
        await client.aclose()
