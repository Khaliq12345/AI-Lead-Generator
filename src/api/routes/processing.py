from fastapi import APIRouter, HTTPException, BackgroundTasks
from src.services.redis_services import get_redis_values, flush_redis_db
from src.services.ai_analysis import ai_analysis

router = APIRouter(prefix="", responses={404: {"description": "Not found"}})

# Start Processing
@router.get("/start-processing", response_model=dict)
async def start_processing(property_details: str, compose_email_prompt: str, background_tasks: BackgroundTasks, number_of_domains:int = 10):
    try:
        # Set Backgroung Processing
        background_tasks.add_task(ai_analysis, property_details, compose_email_prompt, number_of_domains)
        
        return {"status": "success", "message": "AI Analysis started in background"}
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# Get Logs
@router.get("/get-log", response_model=str)
async def get_log():
    try:
        value = await get_redis_values()
        return value
    except Exception as e:
        raise HTTPException(500, detail=str(e))
     
# @router.post("/test", response_model=None)
# async def set_log():
#     property_details = "I want to sell a spacious house in Riviera South with large rooms and a luxury kitchen."
#     number_of_domains = 10
#     res = generate_company_domains(property_details,number_of_domains)
#     print(res)
    
# Clear Logs
@router.get("/flush-db", response_model=None)
async def flush_db():
    try:
        await flush_redis_db()
        return "sucess"
    except Exception as e:
        raise HTTPException(500, detail=str(e))
