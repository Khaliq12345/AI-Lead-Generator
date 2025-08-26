from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from src.services.scraper_service import run
import os

router = APIRouter(prefix="", responses={404: {"description": "Not found"}})


# Start Scraping
@router.get("/scrape-link", response_model=str)
def scrap_link(url: str):
    try:
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "..", "..", "services", "rel.json")
        file_path = os.path.abspath(file_path)
        if not os.path.isfile(file_path):
            raise HTTPException(400, detail="Unable to Find Session File rel.json")
        output_path = run(url)
        if not output_path:
            raise HTTPException(400, detail=f"Unable to Scrape the url : {url}")
        # return output_path
        return FileResponse(
        path=file_path,
        filename=output_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    except Exception as e:
        raise HTTPException(500, detail=str(e))
