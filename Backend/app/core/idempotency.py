from fastapi import Header, HTTPException, Depends
from app.models.user import User
from app.auth.oauth2 import get_current_user
from app.core.redis import redis_client

async def check_idempotency(
    current_user: User = Depends(get_current_user),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")
):
    if not idempotency_key:
        return 

    cache_key = f"idempotency:{current_user.id}:{idempotency_key}"
    
    already_processed = await redis_client.get(cache_key)
    
    if already_processed:
        raise HTTPException(status_code=409, detail="Request already processed.")
    
    await redis_client.set(cache_key, "processed", ex=86400)
