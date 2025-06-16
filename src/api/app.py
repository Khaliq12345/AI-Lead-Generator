import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes.processing import router as processing_router
from src.api.routes.logs import router as logs_router
from src.core.config import ENV

app = FastAPI(
    title="AI Lead Generator API",
    description="API with required EndPoints - Structured",
    version="1.0.0",
)
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(prefix="/api", router=processing_router, tags=["Processing"])
app.include_router(prefix="/api", router=logs_router, tags=["Logs"])


def start_app():
    uvicorn.run(
        "src.api.app:app",
        host="localhost",
        port=8000,
        reload=ENV != "prod",
    )
