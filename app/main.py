import sys
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers.example import router as example
from routers.solution import router as backend
from utils.logging import get_app_logger

logger = get_app_logger(name="FONOMA_BACKEND")
logger.info("Fonoma Backend Test")

app = FastAPI(title="fonoma-backend-test")

headers = {
    "Content-Type",
    "X-Amz-Date",
    "Authorization",
    "X-Api-Key",
    "X-Amz-Security-Token",
    "X-Amz-User-Agent",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Credentials",
    "Access-Control-Allow-Origin"
}

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = headers,
)

app.include_router(backend.router)
app.include_router(example.router)

@app.middleware("http")
async def request_logger(request: Request, call_next):
    response = await call_next(request)
    return response