from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.processing import router as processing_router


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
app.include_router(prefix="/api", router=processing_router, tags=["Main Routes"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "__main__:app",
        host="localhost",
        port=8000,
        reload=True,
    )
