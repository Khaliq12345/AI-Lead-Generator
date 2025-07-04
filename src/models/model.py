from typing import List
from pydantic import BaseModel


# Define the Mail response model
class MailResponse(BaseModel):
    subject: str
    body: str
    send_from: str
    send_to: str


# Define the Domain response model
class DomainResponse(BaseModel):
    links: list[str]


class Lead(BaseModel):
    email: str
    lead_type: str
    first_name: str
    last_name: str
    position: str
    phone_number: str
    domain: str


class Leads(BaseModel):
    leads: List[Lead]
