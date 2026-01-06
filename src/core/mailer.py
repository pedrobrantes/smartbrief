import requests
from src.settings import RESEND_API_KEY

def send_email(to_email, subject, html_content):
    if not RESEND_API_KEY:
        raise ValueError("RESEND_API_KEY is missing in settings.")

    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "from": "SmartBrief <onboarding@resend.dev>",
        "to": [to_email],
        "subject": subject,
        "html": html_content
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    
    return response.json()
