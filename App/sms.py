import os
import requests

def send_sms(phone_number, message_text):
    base_url = os.getenv("INFOBIP_BASE_URL")
    api_key = os.getenv("INFOBIP_API_KEY")
    sender = os.getenv("INFOBIP_SENDER")

    url = f"https://{base_url}/sms/2/text/advanced"
    headers = {
        "Authorization": f"App {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "messages": [
            {
                "destinations": [{"to": phone_number}],
                "from": sender,
                "text": message_text
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"SMS sent to {phone_number}: {message_text}")
        return response.json()
    except Exception as e:
        print(f" Failed to send SMS to {phone_number}: {e}")
        return None