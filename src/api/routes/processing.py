from fastapi import APIRouter, HTTPException, BackgroundTasks
from src.services.ai_analysis import ai_analysis
# from src.services.generate_company_domains import generate_company_domains

router = APIRouter(prefix="", responses={404: {"description": "Not found"}})

# Start Processing
@router.get("/start-processing", response_model=dict)
async def start_processing(property_details: str, compose_email_prompt: str, background_tasks: BackgroundTasks, number_of_domains:int = 10) -> dict:
    try:
        # Set Backgroung Processing
        background_tasks.add_task(ai_analysis, property_details, compose_email_prompt, number_of_domains)
        return {"status": "success", "message": "AI Analysis started in background"}
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# @router.post("/test", response_model=None)
# async def set_log() -> str:
#     property_details = "I want to sell a spacious house in Riviera South with large rooms and a luxury kitchen."
#     number_of_domains = 2
#     res = generate_company_domains(property_details,number_of_domains)
#     print(res)
#     return str(res)