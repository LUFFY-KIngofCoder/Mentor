from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk
import uuid
import time
from contextlib import asynccontextmanager

from app.core.exceptions import AppException,app_exception_handler
from app.api.user import router as user_router
from app.api.commitment import router as commitment_router
from app.api.daily_entry import router as daily_entry_router
from app.api.tracking_metric import router as tracking_metric_router
from app.api.missed_day_reflection import router as missed_day_reflection_router
from app.api.execution_log import router as execution_log_router
from app.api.analytics import router as analytics_router
from app.core.config import settings
from app.core.logger import request_id_var, logger
from app.db.database import engine

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    send_default_pii=True,
    traces_sample_rate=1.0,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI Server starting up...")
    
    yield
    
    logger.info("FastAPI Server shutting down. Closing Database connections...")
    await engine.dispose()
    logger.info("Database connections cleanly closed.")


app = FastAPI(lifespan=lifespan)


# Exception Handler
app.add_exception_handler(AppException, app_exception_handler)

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

@app.middleware("http")
async def add_request_id_and_timing_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    request_id_var.set(request_id)
    start_time = time.time()

    #Pass the req to router
    response = await call_next(request)

    process_time = time.time() - start_time

    # Send Tracing info back to user
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)

    logger.info(f"Processed request to {request.url.path} in {process_time:.4f}s")    

    return response
    

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
async def api_root():
    return {"message": "Mentor API v1.0"}

@api_router.get("/health")
async def health_check():
    return {"status": "healthy"}

@api_router.get("/sentry-debug")
async def trigger_error():
    # pyrefly: ignore [division-by-zero]
    division_by_zero = 1 / 0



# Mount everything to the app
app.include_router(api_router)