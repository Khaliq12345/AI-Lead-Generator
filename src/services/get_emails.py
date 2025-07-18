import json
import httpx
from src.core import config
from typing import List, Dict
from urllib.parse import urlparse

from src.models.model import Leads
from src.services.redis_services import set_redis_value
from openai import OpenAI

client = OpenAI(api_key=config.OPENAI_KEY)


def extract_domain(url) -> str:
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname or parsed_url.path
    if hostname.startswith("www."):
        hostname = hostname[4:]
    return hostname


def fetch_emails_from_domain(
    domain: str,
) -> List[Dict]:
    """Contacte l'API Hunter.io et retourne les e-mails associés à un domaine."""
    url = "https://api.hunter.io/v2/domain-search"
    params = {
        "domain": extract_domain(domain),
        "api_key": config.HUNTER_API_KEY,
    }

    try:
        response = httpx.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("data", {}).get("emails", [])
    except httpx.HTTPError as e:
        print(f"Erreur lors de la requête : {e}")
        return []


def filter_emails(
    emails: List[Dict],
) -> List[Dict]:
    """Filtre les e-mails ayant un seniority à 'executif'."""
    return [
        {
            "email": email.get("value"),
            "type": email.get("type"),
            "first_name": email.get("first_name"),
            "last_name": email.get("last_name"),
            "position": email.get("position"),
            "position_raw": email.get("position_raw"),
            "seniority": email.get("seniority"),
            "phone_number": email.get("phone_number"),
        }
        for email in emails
        if email.get("seniority") == "executive"
    ]


def filter_emails_with_ai(lead_info: list[Dict], domain: str) -> List[Dict]:
    prompt = f"""
    You are an AI assistant who helps identify leads that are involve in acquisitions or investment decisions.
    You are provided with a list of leads in a dict with some information like name, email, phone and position,
    Your task is to filter and return only executive that are involve in acquisitions or investment decisions.
    Position like - 
    Head of Acquisitions
    Chief Investment Officer
    Managing Principal
    Asset Manager
    Portfolio Manager
    SVP/EVP of Real Estate or Development
    Executive Director
    CEO, President (only if involved in acquisitions or investment decisions)

    Leads: {lead_info}
    Domain: {domain}
    """.strip()

    # Generate the
    try:
        contents = []
        contents.append(
            {
                "type": "text",
                "text": "Filter the leads to have only executive that are involve in acquisitions or investment decisions.",
            }
        )

        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            temperature=0.2,
            max_tokens=300,
            messages=[
                {"role": "system", "content": prompt},
                {
                    "role": "user",
                    "content": contents,
                },
            ],
            response_format=Leads,
        )

        parsed = completion.choices[0].message.parsed
        if not parsed:
            return []
        leads = json.loads(parsed.model_dump_json())
        leads = [lead for lead in leads.get("leads", [])]
        return leads
    except Exception as e:
        print(f"Error filtering leads - {e}")
    return []


# Main function
def main_extract_domain(
    domain: str,  # ex : https://www.stripe.com/
) -> List[Dict]:
    # extract_domain(DOMAIN)
    try:
        emails = fetch_emails_from_domain(domain)
        if not emails:
            print("Aucun emails pour le domaine trouvé ou erreur d'appel.")
            return []
        filtered = filter_emails(emails)
        ai_filtered = filter_emails_with_ai(filtered, domain)
        return ai_filtered
    except Exception as e:
        set_redis_value(
            f"----- Got Error while extracting domain's emails : {str(e)}"
        )
        return []
