import requests
import os

from dotenv import load_dotenv


load_dotenv()

api_data = []

def request_info():
    url = os.getenv("WIX_SERVICES_URL")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Authorization": os.getenv("WIX_API_KEY"),
        "wix-site-id": os.getenv("WIX_SITE_ID"),
    }

    payload = {
        "query": {}
    }

    return url, headers, payload

def get_services_data():
    global api_data

    url, headers, payload = request_info()

    response = requests.post(url, headers=headers, json=payload)
    response = response.json()

    for service in response['services']:
        api_data.append({
            'id': service['id'],
            'name': service['name'],
            'description': service['description'],
            'tagLine': service['tagLine'],
            'category': service['category'],
            'form': service['form'],
            'payment': service['payment'],
            'onlineBooking': service['onlineBooking']['enabled'],
            'locations': service['locations']
        })
