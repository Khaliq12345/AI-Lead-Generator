import os
import zipfile
from pathlib import Path
from src.services.get_emails import main_extract_domain
from src.services.generate_company_domains import (
    generate_company_domains,
    generate_email_leads,
)
from src.services.redis_services import set_redis_value


def folder_to_zip(folder: str | Path):
    zip_path = os.path.join(folder, "mails.zip")
    print(zip_path)
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for idx, file in enumerate(os.listdir(folder)):
            if ".md" not in file:
                continue
            file_path = os.path.join(
                folder, file
            )  # Write file with relative path (preserve folder structure)
            zipf.write(file_path, f"mail_{idx}.md")

    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        os.remove(file_path) if ".md" in file_path else None


def get_leads(
    tasks: dict,
    task_id: str,
    property_details: str,
    lead_type: str,
    number_of_domains: int = 10,
    base64_string: str = "",
) -> None:
    outputs_text = ""
    try:
        set_redis_value(
            "- Strating Analysis ... \n- Trying to get Company domains from provided property_details ..."
        )
        leads = generate_email_leads(
            property_details,
            number_of_domains=number_of_domains,
            base64_string=base64_string,
            lead_type=lead_type,
        )
        # company_domains: list[str] = generate_company_domains(
        #     property_details,
        #     number_of_domains=number_of_domains,
        #     base64_string=base64_string,
        # )
        # set_redis_value(
        #     f"- We Found {len(company_domains)} Company Domains.\n- Starting loop on them ..."
        # )
        # for i, company_domain in enumerate(company_domains):
        #     emails = main_extract_domain(company_domain)
        #     set_redis_value(
        #         f"----- Progress : {i + 1} / {len(company_domains)} ---> {100 * (i + 1) / len(company_domains)} %  -----"
        #     )
        for lead in leads:
            for key in lead.keys():
                outputs_text += f"{key.capitalize()}: {lead[key]}\n"
            outputs_text += "-------------\n"

        tasks[task_id]["data"] = outputs_text
        tasks[task_id]["status"] = "success"
    except Exception as e:
        print(f"Error - {e}")
        set_redis_value(
            f"----- Got Error : {str(e)}\n--------------- Analysis Unfortunately Ended  ---------------"
        )
        tasks[task_id]["status"] = "failed"
