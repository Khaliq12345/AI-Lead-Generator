from src.services import compose_email
from src.api.app import start_app

property_info = """ 
Longwood Bronx Development Opportunity


18K SF L-shaped lot with 148 feet of frontage
C8-3 zoning with 37,576 – 122,122 BSF with possibility to expand
located along the I-95 commercial corridor just off of I-278/Bruckner Expy
Ideal site for medical, shelter, nursing home, charter school, and more
Asking Price: $10,750,000. Find me the most likely buyer for the above and attached property please include website, final decision maker for real estate investments,
and email address. Its ideal for medical, shelter, nursing home, charter school,
"""

if __name__ == "__main__":
    print("Hello world!")
    start_app()
    # with open("input.pdf", "w+") as f:
    #     merger = PdfMerger(fileobj=f)
    # with open("test.pdf", "rb") as f:
    #     merger = merger.append(io.BytesIO(f.read()))
    #
    # if merger:
    #     merger.close()
    #
    # with open("input.pdf", "rb") as f:
    #     base64_string = base64.b64encode(f.read()).decode("utf-8")
    #     print(base64_string)
    # compose_email.generate_lead_email(
    #     send_from="test@gmail.com",
    #     send_to="client@gmail.com",
    #     lead_name="Client",
    #     lead_position="Client Position",
    #     property=property_info,
    #     base64_string=base64_string,
    # )
