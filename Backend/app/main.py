from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.user import router as user_router
from app.api.commitment import router as commitment_router
from app.api.daily_entry import router as daily_entry_router
from app.api.tracking_metric import router as tracking_metric_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

app.include_router(user_router)
app.include_router(commitment_router)
app.include_router(tracking_metric_router)
app.include_router(daily_entry_router)


@app.get("/")
def root():
    return {"message": "Mentor Backend Running"}