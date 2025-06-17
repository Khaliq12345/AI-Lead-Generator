import json
from openai import OpenAI
from src.core import config
from src.models.model import DomainResponse, Leads
from src.services.redis_services import set_redis_value

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=config.OPENAI_KEY)


def generate_email_leads(
    property_details: str, number_of_domains: int, base64_string: str = ""
) -> list[str]:
    # Construct the prompt
    prompt = f"""
    You are an AI assistant who helps identify potential executive from different companies that could be interested in a specific property or offer.
    You are provided with the description of a property or product through an input called 'property_details' and a pdf.
    Your task is to find a list of real company website domains that are most likely to be interested in the described property. Only include relevant company domains that could realistically be interested in the offer, based on the details provided.
    You should only return only executive that are involve in acquisitions or investment decisions in each domains.
    The total number of domains to return is {number_of_domains}.
    NOTE: DO NOT RETURN COMPANIES OR EXECUTIVE THAT ARE NOT REAL.
    IF THEIR INFORMATION IS NOT AVAILABLE IN YOUR DATABASE DO NOT MODIFY
    Here is the property description:
    {property_details}
    """.strip()

    # Generate the
    try:
        contents = []
        if base64_string:
            contents.append(
                {
                    "type": "file",
                    "file": {
                        "filename": "input.pdf",
                        "file_data": f"data:application/pdf;base64,{base64_string}",
                    },
                }
            )

        contents.append(
            {
                "type": "text",
                "text": "Provide the information of all the executives that are involve in the decision making of real estate acquisitions",
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
            response_format=Leads,
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


def generate_company_domains(
    property_details: str, number_of_domains: int, base64_string: str = ""
) -> list[str]:
    # Construct the prompt
    prompt = f"""
    You are an AI assistant who helps identify potential company domains that could be interested in a specific property or offer.
    You are provided with the description of a property or product through an input called 'property_details' and a pdf.
    Your task is to think critically and generate a list of N company website domains that are most likely to be interested in the described property. Only include relevant company domains that could realistically be interested in the offer, based on the details provided.
    Return the results as a plain list of website domains (URLs), one per line, like this:
    https://www.company1.com/
    https://www.company2.com/
    https://www.company3.com/
    Do not include explanations, summaries, bullet points, or any extra text—only the list of domains.
    The total number of domains to return is {number_of_domains}.
    Here is the property description:
    {property_details}
    """.strip()

    # Generate the
    try:
        contents = []
        if base64_string:
            contents.append(
                {
                    "type": "file",
                    "file": {
                        "filename": "input.pdf",
                        "file_data": f"data:application/pdf;base64,{base64_string}",
                    },
                }
            )

        contents.append(
            {
                "type": "text",
                "text": "Provide the company domains based on the pdf and propert details",
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
            response_format=DomainResponse,
        )

        message_text = completion.choices[0].message.parsed
        if not message_text:
            return []
        return message_text.links
    except Exception as e:
        set_redis_value(
            f"----- Got Error while generating company domains : {str(e)}"
        )
        return []
