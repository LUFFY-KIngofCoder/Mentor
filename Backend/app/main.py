from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware


from app.api.user import router as user_router
from app.api.commitment import router as commitment_router
from app.api.daily_entry import router as daily_entry_router
from app.api.tracking_metric import router as tracking_metric_router
from app.api.missed_day_reflection import router as missed_day_reflection_router
from app.api.execution_log import router as execution_log_router
from app.api.analytics import router as analytics_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://65.2.70.233:3000",
        "http://localhost",
        "http://65.2.70.233"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

# Master API Router
api_router = APIRouter(prefix="/api")

# Sub-routers
api_router.include_router(user_router)
api_router.include_router(commitment_router)
api_router.include_router(tracking_metric_router)
api_router.include_router(daily_entry_router)
api_router.include_router(missed_day_reflection_router)
api_router.include_router(execution_log_router)
api_router.include_router(analytics_router)

# Health & Root info attached to /api
@api_router.get("/")
def api_root():
    return {"message": "Mentor API v1.0"}
@api_router.get("/health")
def health_check():
    return {"status": "healthy"}

# Mount everything to the app
app.include_router(api_router)