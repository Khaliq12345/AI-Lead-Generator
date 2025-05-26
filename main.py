from src.services.compose_email import generate_lead_email

def main():
    print("Hello from ai-lead-generator!")
    
    email = generate_lead_email(
        send_from="client@gmail.com",
        send_to="lead@gmail.com",
        lead_name="John Doe",
        lead_position="sales executive",
        property="Its a House, with a hall, two chambers very spacefull and others, bathroom, kitchen ... everything you can imagine",
        additional_prompt="Mention our new product launch and encourage him to book a demo."
    )

    print(email.model_dump())


if __name__ == "__main__":
    main()
