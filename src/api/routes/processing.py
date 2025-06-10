import shutil
import os
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile
from src.services.ai_analysis import ai_analysis
from src.services.pdf_service import convert_image_to_pdf
from src.core.config import STATUS_FILE
from PyPDF2 import PdfMerger
from datetime import datetime
import base64

router = APIRouter(prefix="", responses={404: {"description": "Not found"}})


# Start Processing
@router.post("/start-processing", response_model=dict)
async def start_processing(
    background_tasks: BackgroundTasks,
    property_details: str,
    compose_email_prompt: Optional[str] = None,
    number_of_domains: int = 10,
    files: Optional[list[UploadFile]] = [],
) -> dict:
    try:
        print(files)
        folder = str(int(datetime.now().timestamp()))
        folder_path = Path(folder)
        folder_path.mkdir(exist_ok=True)
        folder_absolute_path = folder_path.absolute().as_posix()
        print(folder_absolute_path)
        base64_string = ""
        if files:
            for file in files:
                with open(f"{folder_absolute_path}/{file.filename}", "wb") as f:
                    f.write(await file.read())

            # loop through all the files and convert them all into one pdf file
            merger = PdfMerger()
            for file in os.listdir(folder_absolute_path):
                if ".pdf" in file:
                    merger.append(f"{folder_absolute_path}/{file}")
                    continue
                output_file = convert_image_to_pdf(
                    f"{folder_absolute_path}/{file}",
                    f"{folder_absolute_path}/{file}.pdf",
                )
                merger.append(output_file) if output_file else None
            merger.write(f"{folder_absolute_path}/{folder}.pdf")
            merger.close()

            # get the base64 format
            with open(f"{folder_absolute_path}/{folder}.pdf", "rb") as f:
                data = f.read()

            base64_string = base64.b64encode(data).decode("utf-8")

            # delete the folder
            shutil.rmtree(folder_absolute_path)

        # Set Processing
        background_tasks.add_task(
            ai_analysis,
            property_details,
            compose_email_prompt,
            number_of_domains,
            base64_string,
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
