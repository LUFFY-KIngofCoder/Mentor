from fastapi import FastAPI
from app.api.user import router as user_router
from app.api.commitment import router as commitment_router
from app.models import Commitment

app = FastAPI()

app.include_router(user_router)
app.include_router(commitment_router)
@app.get("/")
def root():
    return {"message": "Mentor Backend Running"}