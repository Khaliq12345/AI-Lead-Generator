import shutil
import os
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile
from src.services.ai_analysis import get_leads, get_sellers_leads
from src.services.compose_email import generate_lead_email
from src.services.pdf_service import convert_image_to_pdf
from PyPDF2 import PdfMerger
from datetime import datetime
import base64
from enum import Enum

router = APIRouter(prefix="", responses={404: {"description": "Not found"}})


class LeadType(Enum):
    BUYING = "buying"
    SELLING = "selling"


tasks = {}


def convert_files_to_base64(files: List[UploadFile]) -> str:
    folder = str(int(datetime.now().timestamp()))
    folder_path = Path(folder)
    folder_path.mkdir(exist_ok=True)
    folder_absolute_path = folder_path.absolute().as_posix()
    base64_string = ""
    if files:
        for file in files:
            with open(f"{folder_absolute_path}/{file.filename}", "wb") as f:
                contents = file.file.read()
                f.write(contents)

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
    return base64_string


@router.post("/get-leads")
def get_lead_route(
    background_tasks: BackgroundTasks,
    property_details,
    number_of_domains,
    lead_type: LeadType,
    files: List[UploadFile] = [],
) -> Optional[str]:
    task_id = str(int(datetime.now().timestamp()))
    tasks[task_id] = {"status": "running", "data": None}
    try:
        base64_string = convert_files_to_base64(files)
        background_tasks.add_task(
            get_leads,
            property_details=property_details,
            number_of_domains=number_of_domains,
            base64_string=base64_string,
            tasks=tasks,
            task_id=task_id,
            lead_type=lead_type.value,
        )
        return task_id
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    

@router.post("/get-sellers-leads")
def get_sellers_lead_route(
    background_tasks: BackgroundTasks,
    property_details,
    number_of_domains,
) -> Optional[str]:
    task_id = str(int(datetime.now().timestamp()))
    tasks[task_id] = {"status": "running", "data": None}
    try:
        background_tasks.add_task(
            get_sellers_leads,
            property_details=property_details,
            number_of_domains=number_of_domains,
            tasks=tasks,
            task_id=task_id,
        )
        return task_id
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)


@router.post("/generate-mail", response_model=str)
def generate_mail(
    client_name: str,
    lead_mail: str,
    lead_name: str,
    lead_position: str,
    property_details: str,
    additional_prompt: str,
    files: List[UploadFile] = [],
) -> Optional[str]:
    try:
        base64_string = convert_files_to_base64(files)
        compose_email = generate_lead_email(
            send_from=client_name,
            send_to=lead_mail,
            lead_name=lead_name,
            lead_position=lead_position,
            property=property_details,
            additional_prompt=additional_prompt,
            base64_string=base64_string,
        )
        if compose_email:
            return (
                f"**Subject** - {compose_email.subject}\n\n{compose_email.body}"
            )
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)


@router.get("/check-status")
def check_status(task_id: str) -> Optional[dict]:
    return tasks.get(task_id) 
