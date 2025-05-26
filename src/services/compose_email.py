import requests
from pydantic import BaseModel
from typing import Optional
from config import config

# API Key
OPENAI_API_KEY = config.OPENAI_KEY

# Structure
class MailResponse(BaseModel):
    subject: str
    body: str
    send_from: str
    send_to: str

def generate_lead_email(send_from: str, send_to: str, lead_name: str, lead_position: str, additional_prompt: Optional[str] = None) -> MailResponse:
    # Main Prompt
    system_prompt = f"""
        You are an AI assistant that writes professional, concise, and engaging emails to potential clients (leads).
        Your goal is to generate an email that includes a clear subject line and a short, persuasive, and polite body.
        The email must sound neutral, friendly, and ready to send as-is, with no placeholders or missing information.
        Do not mention any company name, position, contact details, or personal details about the sender—only use the information provided.
        Write the email as if it is coming from {send_from} and being sent to {send_to}.
        The lead's name is {lead_name} and their position is {lead_position}. Address them directly by name in a respectful and professional manner.
        Do not ask the recipient to fill in any information.
        Do not include any placeholders like [Your Name], [Your Position], or similar—absolutely no placeholders.
        If any additional instructions are provided, follow them carefully.
        Output only the subject and the body of the email in a structured format, exactly like this:
        {{
        "subject": "...",
        "body": "..."
        }}
        No extra information or explanations.
        """


    # If any Addition
    if additional_prompt:
        system_prompt += f"\nAdditional context: {additional_prompt}"

    # Setting Up
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Please provide the subject and body of the email."}
        ],
        "max_tokens": 300
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json=payload
    )

    response.raise_for_status()
    content = response.json()

    # Extraction
    message_text = content['choices'][0]['message']['content']

    # Analysing
    subject_line = ""
    body_text = ""

    for line in message_text.splitlines():
        if line.lower().startswith("subject:"):
            subject_line = line.split(":", 1)[1].strip()
        elif line.lower().startswith("body:"):
            body_text = line.split(":", 1)[1].strip()
        else:
            body_text += "\n" + line.strip()

    # Re Structure using Pydantic
    return MailResponse(
        subject=subject_line,
        body=body_text.strip(),
        send_from=send_from,
        send_to=send_to
    )
