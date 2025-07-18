import json
from openai import OpenAI
from src.core import config
from src.models.model import SellerLeads
from src.services.redis_services import set_redis_value

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=config.OPENAI_KEY)


def generate_sellers_email_leads(
    property_details: str,
    number_of_domains: int,
) -> list[str]:
    # Construct the prompt
    prompt = f"""
    You are an AI assistant specialized in identifying real acquisition or investment executives from legitimate companies who may be interested in a specific type of unsold or off-market property.
    You are provided with the description of a commercial property or asset via an input called 'property_details', as well as a PDF for reference.
    Your task is to identify and return a list of real company website domains (maximum: {number_of_domains}) representing companies that are most likely to be interested in acquiring or investing in this type of property, based on the details provided.
    You must only include:
    - Companies that are actively involved in commercial property acquisitions or real estate investments.
    - Verified executives at those companies who are directly responsible for acquisition, investment, or portfolio decisions.
    - Their real names, verified emails, professional roles, and the company domain.
    DO NOT:
    - Return companies or executives that do not exist.
    - Invent or modify data.
    - Include brokers or non-investment personnel.
    Example Prompt:
    Show me off-market shopping centers in New Jersey that were listed from 2021 to 2023 but never sold.
    Expected Output Format (for each match):
    - Company Name: [Name]
    - Website: [www.companydomain.com]
    - Executive Name: [Full Name]
    - Role: [Title related to acquisitions or investments]
    - Email: [Verified email]
    - Phone: [If available]
    Here is the property description:
    {property_details}
    """.strip()
    try:
        contents = []
        contents.append(
            {
                "type": "text",
                "text": "Show me off-market shopping centers in New Jersey that were listed from 2021 to 2023 but never sold.",
            }
        )
        completion = client.beta.chat.completions.parse(
            store=True,
            model="gpt-4.1",
            temperature=0.2,
            max_tokens=2048,
            messages=[
                {"role": "system", "content": prompt},
                {
                    "role": "user",
                    "content": contents,
                },
            ],
            response_format=SellerLeads,
        )
        parsed = completion.choices[0].message.parsed
        if not parsed:
            return []
        leads = json.loads(parsed.model_dump_json())
        leads = [lead for lead in leads.get("leads", [])]
        return leads
    except Exception as e:
        set_redis_value(
            f"----- Got Error while generating company domains : {str(e)}"
        )
        return []

