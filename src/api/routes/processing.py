from typing import Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from src.services.ai_analysis import ai_analysis
from src.core.config import STATUS_FILE

router = APIRouter(prefix="", responses={404: {"description": "Not found"}})


# Start Processing
@router.post("/start-processing", response_model=dict)
async def start_processing(
    background_tasks: BackgroundTasks,
    property_details: str,
    compose_email_prompt: Optional[str] = None,
    number_of_domains: int = 10,
) -> dict:
    try:
        # Set Processing
        background_tasks.add_task(
            ai_analysis,
            property_details,
            compose_email_prompt,
            number_of_domains,
        )
        return {
            "message": "AI Analysis started in background",
        }
    except Exception as e:
        raise HTTPException(500, detail=str(e))


@router.get("/check-status")
def check_status() -> dict:
    with open(STATUS_FILE, "r") as f:
        status = f.read()
        status_split = status.split(":")
        if len(status_split) == 2:
            return {"status": status_split[0], "folder": status_split[-1]}
        else:
            return {"status": status_split[0]}
