from typing import Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from src.services.ai_analysis import ai_analysis

router = APIRouter(prefix="", responses={404: {"description": "Not found"}})


# Start Processing
@router.get("/start-processing", response_model=dict)
async def start_processing(
    background_tasks: BackgroundTasks,
    property_details: str,
    compose_email_prompt: Optional[str] = None,
    number_of_domains: int = 10,
    test: bool = True,
) -> dict:
    try:
        # Set Backgroung Processing
        background_tasks.add_task(
            ai_analysis,
            test,
            property_details,
            compose_email_prompt,
            number_of_domains,
        )
        return {
            "status": "success",
            "message": "AI Analysis started in background",
        }
    except Exception as e:
        raise HTTPException(500, detail=str(e))

