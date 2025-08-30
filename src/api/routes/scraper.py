from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from src.core import config
from src.services.scraper_service import run
import os

router = APIRouter(prefix="", responses={404: {"description": "Not found"}})


# Start Scraping
@router.get("/scrape-link", response_model=str)
def scrap_link(url: str):
    try:
        if not os.path.isfile(config.REL_PATH or ""):
            raise HTTPException(400, detail="Unable to Find Session File rel.json")
        content = run(url)
        return JSONResponse(content=content)
    except Exception as e:
        raise HTTPException(500, detail=str(e))
