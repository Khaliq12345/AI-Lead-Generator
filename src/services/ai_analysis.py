import os
import zipfile
from pathlib import Path
import datetime
from typing import Optional
from src.core import config
from src.services.get_emails import main_extract_domain
from src.services.generate_company_domains import generate_company_domains
from src.services.compose_email import generate_lead_email
from src.services.redis_services import set_redis_value


def update_status(value: str):
    with open(config.STATUS_FILE, "w") as f:
        f.write(f"{value}")


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


async def ai_analysis(
    property_details: str,
    compose_email_prompt: Optional[str] = None,
    number_of_domains: int = 10,
    base64_string: str = "",
) -> None:
    output_folder = "./outputs"
    Path(output_folder).mkdir(exist_ok=True)
    folder = int(datetime.datetime.now().timestamp())
    folder_path = Path(f"{output_folder}/{folder}")
    folder_path.mkdir(exist_ok=True)
    absolute_path = folder_path.absolute().as_posix()
    update_status("running")
    try:
        await set_redis_value(
            "- Strating Analysis ... \n- Trying to get Company domains from provided property_details ..."
        )
        company_domains: list[str] = generate_company_domains(
            property_details,
            number_of_domains=number_of_domains,
            base64_string=base64_string,
        )
        await set_redis_value(
            f"- We Found {len(company_domains)} Company Domains.\n- Starting loop on them ..."
        )
        for i, company_domain in enumerate(company_domains):
            await set_redis_value(
                f"--- Dealing with domain number {i + 1} : {company_domain}. We're trying to extract emails"
            )
            emails = main_extract_domain(company_domain)
            await set_redis_value(
                f"--- Email Extraction ended. We've got {len(emails)} emails for this domain.\n--- Extraction results : {str(emails)}\n--- Starting loop on them ..."
            )
            for j, email in enumerate(emails):
                await set_redis_value(
                    f"----- Composing Email number {j + 1} with : {email} as mail receiver ..."
                )
                compose_email = generate_lead_email(
                    send_from=config.CLIENT_EMAIL,
                    send_to=email["email"],
                    lead_name=f"{email['first_name']} {email['last_name']}",
                    lead_position=email["position"],
                    property=property_details,
                    additional_prompt=compose_email_prompt,
                    base64_string=base64_string,
                )
                if compose_email:
                    with open(f"{absolute_path}/{i}_{j}_mail.md", "w") as f:
                        top_message = (
                            f"Name - {email['first_name']} {email['last_name']}"
                            f"\nEmail - {compose_email.send_to}\nDomain - {company_domain}\n"
                            f"Position - {email['position']}"
                        )
                        if compose_email:
                            f.write(
                                f"{top_message}\n--------------------------------------------\n\n"
                                f"# Body\n\n**Subject** - {compose_email.subject}\n\n{compose_email.body}"
                            )
            await set_redis_value(
                f"----- Progress : {i + 1} / {len(company_domains)} ---> {100 * (i + 1) / len(company_domains)} %  -----"
            )
        folder_to_zip(absolute_path)
        await set_redis_value("----- Ending -----\n- Processing Task Ended")
        update_status(f"success:{absolute_path}/mails.zip")
    except Exception as e:
        print(f"Error - {e}")
        await set_redis_value(
            f"----- Got Error : {str(e)}\n--------------- Analysis Unfortunately Ended  ---------------"
        )
        update_status("failed")
