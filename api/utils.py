from django.conf import settings
import requests
import json


def get_payment_url(order):
    url = "https://api.tap.company/v2/charges"

    payload = {
        "amount": f"{order.total}",
        "currency": "SAR",
        "reference": {
            "transaction": "txn_0001",
            "order": f"{order.number}"
        },
        "customer": {
            "first_name": f"{order.user.first_name}",
            "last_name": f"{order.user.last_name}",
            "email": f"{order.user.email}",
            "phone": {
                "country_code": "966",
                "number": f"{order.user.username[1:]}"
            }
        },
        "source": {
            "id": "src_all"
        },
        "post": {
            "url": "https://d3c6eea0d3d8.ngrok.io/api/v1/checkout/complete/"
        },
        "redirect": {
            "url": "https://d3c6eea0d3d8.ngrok.io/api/v1/checkout/thankyou/"
        }
    }

    payload = json.dumps(payload)
    headers = {
        'authorization': f"Bearer {settings.TAP_TOKEN}",
        'content-type': "application/json"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    response = response.json()
    order.status = response['status']
    order.save()
    return response['transaction']['url']