import requests
from django.conf import settings

headers = {
    "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    "Content-Type": "application/json",
}


def verify_payment(reference):
    paystack_url = f"https://api.paystack.co/transaction/verify/{reference}"

    response = requests.get(url=paystack_url, headers=headers)
    return response


# confirm payment dat from paystack
def payment_is_confirm(data, amount):
    try:
        if (
            data.status_code == 200
            and data.json()["status"] == True
            and data.json()["data"].get("status") == "success"
            and data.json()["data"].get("amount") == amount * 100
        ):
            return True
        else:
            return False
    except:
        return False
