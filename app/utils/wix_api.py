import requests
import datetime
import os

from datetime import datetime, timedelta
from dotenv import load_dotenv


load_dotenv()

api_services_data = []
api_staff_data = []
api_availability_data = []
api_booking_data = {}

async def fill_booking_data(key, value):
    api_booking_data[key] = value

async def clear_booking_data():
    api_booking_data.clear()

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
    if api_availability_data:
        return

    today = datetime.now() + timedelta(days=1)
    next_month = today + timedelta(days=30)

    payload = {
        "query": {
            "filter": {
                "serviceId": service_id,
                "startDate": today.strftime('%Y-%m-%dT10:00:00'),
                "endDate": next_month.strftime('%Y-%m-%dT17:30:00')
            }
        },
        "timezone": "Europe/Kyiv"
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

    free = response.get('priceDescriptionInfo', {}).get('original', False) == "Безкоштовно"
    if free:
        return 'Безкоштовно'
    else:
        return response['priceInfo']['calculatedPrice']

async def create_booking(name, slot, customer_name, customer_email):
    headers = await request_info()
    booking_data = {
        "booking": {
            "bookedEntity": {
                "slot": slot,
                "title": name,
                "tags": ["INDIVIDUAL"]
            },
            "contactDetails": {
                "firstName": customer_name,
                "email": customer_email
            },
            "additionalFields": [],
            "totalParticipants": 1
        },
        "sendSmsReminder": False,
        "participantNotification": {
            "notifyParticipants": True
        },
    }

    response = requests.post(os.getenv("WIX_CREATE_BOOKING"), headers=headers, json=booking_data)

    await fill_booking_data('booking_id', response.json()['booking']['id'])

    status = await create_order()
    print(api_booking_data)

    return status

async def create_order():
    headers = await request_info()
    price_amount = api_booking_data['price'] if api_booking_data['slot']['soldier'] == 'no' or api_booking_data['fixed'] == True else int(api_booking_data['price']) / 2

    order_data = {
        "order": {
            "buyerInfo": {
                "firstName": api_booking_data['slot']['firstName'],
                "email": api_booking_data['slot']['email'],
            },
            "priceSummary": {
                "subtotal": {
                    "amount": f"{price_amount}",
                    "formattedAmount": f"{price_amount},00₴"
                },
                "tax": {
                    "amount": "0",
                    "formattedAmount": "0,00₴"
                },
                "total": {
                    "amount": f"{price_amount}",
                    "formattedAmount": f"{price_amount}₴"
                }
            },
            "billingInfo": {
                "contactDetails": {
                    "firstName": api_booking_data['slot']['firstName']
                }
            },
            "status": "APPROVED",
            "lineItems": [
                {
                    "productName": {
                        "original": api_booking_data['slot']['name']
                    },
                    "catalogReference": {
                        "catalogItemId": api_booking_data['booking_id'],
                        "appId": "13d21c63-b5ec-5912-8397-c3a5ddb27a97"
                    },
                    "quantity": 1,
                    "price": {
                        "amount": f"{price_amount}",
                        "formattedAmount": f"{price_amount}₴"
                    },
                    "itemType": {
                        "preset": "SERVICE"
                    },
                    "taxDetails": {
                        "taxableAmount": {
                            "amount": f"{price_amount}",
                            "formattedAmount": f"{price_amount}₴"
                        },
                        "taxRate": "0",
                        "totalTax": {
                            "amount": "0",
                            "formattedAmount": "0,00₴"
                        }
                    }
                }
            ],
            "paymentStatus": "NOT_PAID",
            "balanceSummary": {
                "balance": {
                    "amount": "0",
                    "formattedAmount": "0,00₴"
                }
            },
            "currency": "UAH",
            "channelInfo": {
                "type": "WEB"
            }
        }
    }
    print(order_data)
    print('create_order')
    response = requests.post("https://www.wixapis.com/ecom/v1/orders", headers=headers, json=order_data)
    print(response.status_code)
    print(response.text)
    return response.status_code
