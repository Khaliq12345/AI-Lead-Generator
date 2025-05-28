from src.core import config
from src.services.get_emails import main_extract_domain
from src.services.generate_company_domains import generate_company_domains
from src.services.compose_email import generate_lead_email
from src.models.model import MailResponse
from src.services.redis_services import set_redis_value


async def ai_analysis(property_details: str, compose_email_prompt: str, number_of_domains:int = 10):
    try:
        results: list[MailResponse] = []
        await set_redis_value("- Strating Analysis ... \n- Trying to get Company domains from provided property_details ...")
        company_domains: list[str] = generate_company_domains(property_details, number_of_domains=number_of_domains)
        await set_redis_value(f"- We Found {len(company_domains)} Company Domains.\n- Starting loop on them ...")
        for i, company_domain in enumerate(company_domains):
            await set_redis_value(f"--- Dealing with domain number {i+1} : {company_domain}. We're trying to extract emails")
            emails = main_extract_domain(company_domain)
            await set_redis_value(f"--- Email Extraction ended. We've got {len(emails)} emails for this domain.\n--- Extraction results : {str(emails)}\n--- Starting loop on them ...")
            for j, email in enumerate(emails):
                await set_redis_value(f"----- Composing Email number {j+1} with : {email} as mail receiver ...")
                compose_email = generate_lead_email(send_from=str(config.CLIENT_EMAIL), send_to=email['email'], lead_name=f"{email['first_name']} {email['last_name']}", lead_position=email['position'], property=property_details, additional_prompt=compose_email_prompt)
                await set_redis_value(f"----- Email Composed. Here is it : {compose_email}")
                if compose_email:
                    results.append(compose_email)
            await set_redis_value(f"----- Progress : {i} / {len(company_domains)} ---> {100*i/len(company_domains)} %  -----")
        await set_redis_value(f"----- Ending -----\n- Processing Task Ended: results {results}\n--------------- Successfully ended analysis ---------------")
    except Exception as e:
        await set_redis_value(f"----- Got Error : {str(e)}\n--------------- Analysis Unfortunaltly Ended  ---------------")