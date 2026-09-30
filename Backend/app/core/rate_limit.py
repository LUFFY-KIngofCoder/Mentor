from h11._abnf import status_code
from fastapi import Request, HTTPException
from app.core.redis import redis_client

async def login_rate_limiter(request: Request):
    
    client_ip = request.client.host
    cache_key = f"rate_limit:login:{client_ip}"
    
    current_attempts = await redis_client.get(cache_key)

    if current_attempts and int(current_attempts) >= 5:
        raise HTTPException(status_code=429, detail="Too Many Requests. Try again after 60 seconds")
    
    await redis_client.incr(cache_key)
    if not current_attempts:
        await redis_client.expire(cache_key, 60)
    
    