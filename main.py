from src.services import (
    # generate_company_domains,
    # get_emails,
    # compose_email,
    ai_analysis,
    # send_mail,
)
import asyncio
from src.api.app import start_app

property_info = """ 
Longwood Bronx Development Opportunity


18K SF L-shaped lot with 148 feet of frontage
C8-3 zoning with 37,576 – 122,122 BSF with possibility to expand
located along the I-95 commercial corridor just off of I-278/Bruckner Expy
Ideal site for medical, shelter, nursing home, charter school, and more
Asking Price: $10,750,000. Find me the most likely buyer for the above and attached property please include website, final decision maker for real estate investments , and email address. Its ideal for medical, shelter, nursing home, charter school,
"""


if __name__ == "__main__":
    print("Hello world!")
    send_to = "kiberkhaliq@gmail.com"
    lead_to = "Khaliq"
    lead_position = "Software Eng."
    property = property_info

    # asyncio.run(ai_analysis.ai_analysis(property_info, number_of_domains=2))
    start_app()
