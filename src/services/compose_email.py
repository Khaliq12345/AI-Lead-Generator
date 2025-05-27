import asyncio
from openai import OpenAI
from typing import Optional
from src.core import config
from src.models.model import MailResponse
from src.services.redis_services import set_redis_value 

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=config.OPENAI_KEY)

def generate_lead_email(
    send_from: str,
    send_to: str,
    lead_name: str,
    lead_position: str,
    property: str,
    additional_prompt: Optional[str] = None,
) -> MailResponse | None:
    # Construct the prompt
    prompt = f"""
    You are an AI assistant that writes professional, concise, and engaging emails to potential clients (leads).
    You are provided with key information about a product to sell: {property}
    Your task is to generate an email that includes a clear subject line and a short, persuasive, and polite body.
    The email must sound neutral, friendly, and ready to send as-is, with no placeholders or missing information.
    Absolutely DO NOT include placeholders or incomplete elements like [Your Name], [Your Position], [Your Company], or any similar placeholders—strictly avoid them. The email must be fully complete and require no modifications before sending.
    Do not mention or invent any company name, personal details, or contact information unless explicitly provided. If no information is provided, omit it entirely.
    Write the email as if it is coming from {send_from} and being sent to {send_to}. The lead's name is {lead_name} and their position is {lead_position}. Address them directly by name in a respectful and professional manner.
    Do not ask the recipient to fill in any information or provide any missing details.
    Return only the subject and the body of the email in this exact format:
    Subject: ...
    Body: ...
    Do not add any explanations, summaries, or extra information—just the subject and the body.
    """.strip()

    if additional_prompt:
        prompt += f"\nAdditional context: {additional_prompt}"

    # Generate the response
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            temperature=0.2,
            max_tokens=300,
            messages=[
                {"role": "system", "content": prompt},
                {
                    "role": "user",
                    "content": "Please provide only the subject and body of the email. No more text",
                },
            ],
            response_format=MailResponse
        )

        # Try to Parse the response
        message_text = completion.choices[0].message.parsed
        return message_text
    except Exception as e:
        asyncio.create_task(set_redis_value(f"----- Got Error : {str(e)}\n--------------- Analysis Unfortunately Ended  ---------------"))