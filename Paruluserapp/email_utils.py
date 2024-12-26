import requests
import logging

def send_email(email_to, subject, message):
    url = 'https://api.emailjs.com/api/v1.0/email/send'
    payload = {
        'service_id': 'service_4v4o9sy',
        'template_id': 'template_b8ter7t',
        'user_id': 'ia-QOhpcwXsN3Eu09',
        'template_params': {
            'to_email': email_to,
            'subject': subject,
            'message': message
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Will raise an error for HTTP error codes
        logging.info("Email sent successfully: %s", response.text)
        return response
    except requests.exceptions.HTTPError as http_err:
        logging.error("HTTP error occurred: %s", http_err)
    except Exception as err:
        logging.error("Other error occurred: %s", err)
    return None
