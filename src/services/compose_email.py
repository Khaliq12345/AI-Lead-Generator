from openai import OpenAI
from pydantic import BaseModel
from typing import Optional
from src.core import config
import json

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=config.OPENAI_KEY)


# Define the response model
class MailResponse(BaseModel):
    subject: str
    body: str
    send_from: str
    send_to: str


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
    Here are the key informations about the product to sell {property}
    You are an AI assistant that writes professional, concise, and engaging emails to potential clients (leads).
    Your goal is to generate an email that includes a clear subject line and a short, persuasive, and polite body.
    The email must sound neutral, friendly, and ready to send as-is, with no placeholders or missing information.
    Do not mention any company name, position, contact details, or personal details about the sender—only use the information provided.
    Write the email as if it is coming from {send_from} and being sent to {send_to}.
    The lead's name is {lead_name} and their position is {lead_position}. Address them directly by name in a respectful and professional manner.
    Do not ask the recipient to fill in any information.
    Do not include any placeholders like [Your Name], [Your Position], or similar—absolutely no placeholders.
    If any additional instructions are provided, follow them carefully.
    No extra information or explanations.
    """.strip()

    if additional_prompt:
        prompt += f"\nAdditional context: {additional_prompt}"

    # Generate the response
    completion = client.chat.completions.create(
        model="gpt-4",
        temperature=0.5,
        max_tokens=300,
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": "Please provide only the subject and body of the email. No more text",
            },
        ],
    )

    # Try to Parse the response

    try:
        message_text = completion.choices[
            0
        ].message.content
        print(f"response : {message_text}")
        if not message_text:
            return None
        mail_data = json.loads(message_text)
        return MailResponse(
            subject=mail_data["subject"],
            body=mail_data["body"],
            send_from=send_from,
            send_to=send_to,
        )
    except json.JSONDecodeError:
        # If Failled Get it Customly
        # print("Failed to parse the response into JSON format.")
        subject_line = ""
        body_text = ""
        if not message_text:
            return None
        for line in message_text.splitlines():
            if line.lower().startswith(
                "subject:"
            ):
                subject_line = line.split(":", 1)[
                    1
                ].strip()
            elif line.lower().startswith("body:"):
                body_text = line.split(":", 1)[
                    1
                ].strip()
            else:
                body_text += "\n" + line.strip()

        return MailResponse(
            subject=subject_line,
            body=body_text.strip(),
            send_from=send_from,
            send_to=send_to,
        )
