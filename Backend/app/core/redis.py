import redis.asyncio as redis
from app.core.config import settings
from arq import create_pool
from arq.connections import RedisSettings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

arq_pool = None
async def get_arq_pool():
    global arq_pool
    if not arq_pool:
        # Connect to the exact same Redis server the worker is listening to
        arq_pool = await create_pool(RedisSettings.from_dsn(settings.REDIS_URL))
    return arq_pool