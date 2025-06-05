import shutil
from pathlib import Path
import datetime
from typing import Optional
from src.core import config
from src.services.get_emails import main_extract_domain
from src.services.generate_company_domains import generate_company_domains
from src.services.compose_email import generate_lead_email
from src.services.redis_services import set_redis_value


async def ai_analysis(
    property_details: str,
    compose_email_prompt: Optional[str] = None,
    number_of_domains: int = 10,
) -> str:
    Path("./outputs/").mkdir(exist_ok=True)
    folder = int(datetime.datetime.now().timestamp())
    folder_path = Path(f"./outputs/{folder}")
    folder_path.mkdir(exist_ok=True)
    try:
        await set_redis_value(
            "- Strating Analysis ... \n- Trying to get Company domains from provided property_details ..."
        )
        company_domains: list[str] = generate_company_domains(
            property_details, number_of_domains=number_of_domains
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
                )
                if compose_email:
                    with open(f"{folder_path}/{i}_{j}_mail.md", "w") as f:
                        if compose_email:
                            f.write(
                                f"""Email - {compose_email.send_to}\n--------------------------------------------\n\n# Body\n\n**Subject** - {compose_email.subject}\n\n{compose_email.body}"""
                            )
            await set_redis_value(
                f"----- Progress : {i+1} / {len(company_domains)} ---> {100 * (i+1) / len(company_domains)} %  -----"
            )
        shutil.make_archive(f"{folder_path}/mails", "zip", folder_path)
        await set_redis_value("----- Ending -----\n- Processing Task Ended")
    except Exception as e:
        await set_redis_value(
            f"----- Got Error : {str(e)}\n--------------- Analysis Unfortunately Ended  ---------------"
        )
    return f"{folder_path}/mails.zip"
