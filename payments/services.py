from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from payments.paystack import verify_payment, payment_is_confirm
from products.repository import ProductRepository
import json
from accounts.repository import NotificationRepository
from accounts.utils import normalize_phone
from utils.utils import send_sms_message
from core.repository import ProductTypeRepository
from payments.repository import ProductPaymentRepository


product_repo = ProductRepository()
payment_repo = ProductPaymentRepository()


def verify_product_payment(request, serializer_class):
    serializer = serializer_class(data=request.data)
    ok = HTTP_200_OK
    bad = HTTP_400_BAD_REQUEST
    json_ld = json.loads
    notification_repo = NotificationRepository
    product_type_repo = ProductTypeRepository

    if serializer.is_valid(raise_exception=True):
        reference = request.data.get("reference")
        product_id = request.data.get("product")
        quantity = serializer.validated_data.get("quantity")
        product_type = serializer.validated_data.get("product_type")
        number_of_days = serializer.validated_data.get("number_of_days")
        payment = serializer.save()

        product = product_repo.get_product_by_id(product_id=product_id)
        p_type = product_type_repo.get_type_by_id(type_id=product_type.id)
        result = verify_payment(reference=reference)
        if p_type.type_name == "rental":
            amount_paid = product.product_price*quantity*number_of_days
        else:
            amount_paid = product.product_price*quantity
        if payment_is_confirm(result, amount_paid):
            payment.payment_successful = True
            payment.save()
            if p_type.type_name == "rental":
                subject = "Product Rental"
                message = (
                    "Hello"
                    "Your product has been rented. Check your SMS for a details."
                    )
                status = "info"

                notification_repo.create_notification(user=product.seller, subject=subject, status=status, message=message)
                phone = normalize_phone(str(product.seller.phone))
                send_sms_message(
                    phone=phone,
                    template="product_renter.html",
                    context={"pname": product.product_name, "bname": request.user.first_name, "quantity": quantity, "amount": amount_paid, "bphone": request.user.phone, "days": number_of_days, },
                    )
                phone1 = normalize_phone(str(request.user.phone))
                send_sms_message(
                    phone=phone1,
                    template="product_rentee.html",
                    context={"pname": product.product_name, "bname": request.user.first_name, "quantity": quantity, "amount": amount_paid, "sphone": product.seller.phone, "days": number_of_days, },
                    )
            else:
                subject = "Product Purchase"
                message = (
                    "Hello"
                    "Your product has been purchased. Check your SMS for a details."
                    )
                status = "info"

                notification_repo.create_notification(user=product.seller, subject=subject, status=status, message=message)
                print("phone", product.seller.phone)
                phone = normalize_phone(str(product.seller.phone))
                send_sms_message(
                    phone=phone,
                    template="product_purchasers.html",
                    context={"pname": product.product_name, "bname": request.user.first_name, "quantity": quantity, "amount": amount_paid, "bphone": request.user.phone, },
                    )
                print("phone1", request.user.phone)
                phone1 = normalize_phone(str(request.user.phone))
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


def get_user_payment(request, serializer_class):
    ok = HTTP_200_OK
    user = request.user
    payments = payment_repo.get_user_payment(seller=user)
    data = serializer_class(payments, many=True).data
    context = {
        "status": "success",
        "message": "User Barter Offers",
        "data": data,
    }
    return ok, context
