import requests
import datetime
import os

from datetime import datetime, timedelta
from dotenv import load_dotenv


load_dotenv()

api_services_data = []
api_staff_data = []
api_availability_data = []
api_price_data = []

async def request_info():
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Authorization": os.getenv("WIX_API_KEY"),
        "wix-site-id": os.getenv("WIX_SITE_ID"),
    }

    return headers

async def post_services_data(url=os.getenv("WIX_SERVICES_URL")):
    global api_services_data

    payload = {
        "query": {}
    }

    headers = await request_info()

    response = requests.post(url, headers=headers, json=payload)
    response = response.json()

    for service in response['services']:
        api_services_data.append({
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

async def post_availability(service_id, location_id, url=os.getenv("WIX_AVAILABILITY_URL")):
    global api_availability_data

    today = datetime.now() + timedelta(days=1)
    next_month = today + timedelta(days=30)

    payload = {
        "query": {
            "filter": {
                "serviceId": service_id,
                "startDate": today.strftime('%Y-%m-%d'),
                "endDate": next_month.strftime('%Y-%m-%d')
            }
        }
    }

    headers = await request_info()

    response = requests.post(url, headers=headers, json=payload)
    response = response.json()

    for slot in response['availabilityEntries']:
        slot = slot['slot']
        if slot['location']['id'] == location_id:
            api_availability_data.append(slot)

async def get_staff_data(url=os.getenv("WIX_STAFFS_URL")):
    global api_services_data

    headers = await request_info()

    response = requests.get(url, headers=headers)
    response = response.json()

    for staff in response['resources']:
        if staff['description']:
            api_staff_data.append({
                'id': staff['id'],
                'name': staff['name'],
                'description': staff['description'],
            })

async def get_price_data(service_id, resource_id, url=os.getenv("WIX_PRICE_URL")):
    global api_price_data

    payload = {
        "bookingLineItems": [
            {
                "serviceId": f'{service_id}',
                "resourceId": f'{resource_id}',
                "numberOfParticipants": 1
            }
        ]
    }

    headers = await request_info()

    response = requests.post(url, headers=headers, json=payload)
    response = response.json()

    return response['priceInfo']['calculatedPrice']

