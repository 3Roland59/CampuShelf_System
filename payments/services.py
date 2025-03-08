from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from payments.paystack import verify_payment, payment_is_confirm
from products.repository import ProductRepository
import json
from accounts.repository import NotificationRepository
from accounts.utils import normalize_phone
from utils.utils import send_sms_message


product_repo = ProductRepository()



def verify_product_payment(request, serializer_class):
    serializer = serializer_class(data=request.data)
    ok = HTTP_200_OK
    bad = HTTP_400_BAD_REQUEST
    json_ld = json.loads
    notification_repo = NotificationRepository

    if serializer.is_valid(raise_exception=True):
        reference = serializer.validated_data.get("reference")
        transaction = serializer.validated_data.get("transaction")
        product_id = serializer.validated_data.get("product_id")
        quantity = serializer.validated_data.get("quantity")

        product = product_repo.get_product_by_id(product_id=product_id)
        result = verify_payment(reference=reference)
        amount_paid = product.product_price*quantity
        if payment_is_confirm(result, amount_paid):
            subject = "Product Purchase"
            message = (
            "Hello"
                "Your product has been purchased. Check your SMS for a details."
            )
            status = "info"

            notification_repo.create_notification(user=product.seller, subject=subject, status=status, message=message)
            phone = normalize_phone(product.seller.phone)
            send_sms_message(
                phone=phone,
                template="product_purchasers.html",
                context={"pname": product.product_name, "bname": request.user.first_name, "quantity": quantity, "amount": amount_paid, "bphone": request.user.phone,},
            )
            phone1 = normalize_phone(request.user.phone)
            send_sms_message(
                phone=phone1,
                template="product_purchase.html",
                context={"pname": product.product_name, "bname": request.user.first_name, "quantity": quantity, "amount": amount_paid, "sphone": product.seller.phone},
            )

            context1 = {
                "status": "success",
                "message": "Product payment successful",
                "data": None,
            }
            return (ok, context1)
        else:
            context1 = {
                "status": "failure",
                "message": "Product payment failed",
                "data": {"type": json_ld(result.content)},
            }
            return (bad, context1)
