from pydantic import BaseModel


# Define the Mail response model
class MailResponse(BaseModel):
    subject: str
    body: str
    send_from: str
    send_to: str