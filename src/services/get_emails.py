import asyncio
import httpx
from src.core import config
from typing import List, Dict
from urllib.parse import urlparse

from src.services.redis_services import set_redis_value


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
        print("\n📧 E-mails filtrés renvoyés :")
        for email in filtered:
            print(f" - {email}\n")
        return filtered
    except Exception as e:
        asyncio.create_task(
            set_redis_value(
                f"----- Got Error while extracting domain's emails : {str(e)}"
            )
        )
        return []

