from fastapi import APIRouter, HTTPException
from src.services.redis_services import get_redis_values, flush_redis_db

router = APIRouter(prefix="", responses={404: {"description": "Not found"}})

# Get Logs
@router.get("/get-log", response_model=str)
async def get_log() -> str:
    try:
        value = await get_redis_values()
        return value
    except Exception as e:
        raise HTTPException(500, detail=str(e))
     
# Clear Logs
@router.get("/clear-log", response_model=None)
async def flush_db() -> str:
    try:
        await flush_redis_db()
        return "sucess"
    except Exception as e:
        raise HTTPException(500, detail=str(e))
