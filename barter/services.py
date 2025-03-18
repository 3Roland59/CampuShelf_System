from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from accounts.repository import NotificationRepository
from accounts.utils import normalize_phone
from utils.utils import send_sms_message
from products.repository import ProductRepository


def barter_service(request: Request, serializer_class):
    ok = HTTP_200_OK
    bad = HTTP_400_BAD_REQUEST
    notification_repo = NotificationRepository
    product_repo = ProductRepository()
    serializer = serializer_class(data=request.data)
 
    if serializer.is_valid(raise_exception=True):
        product_id = request.data.get("product")
        product = product_repo.get_product_by_id(product_id=product_id)
        barter = serializer.save()

        subject = "Barter Trade Offer"
        message = (
            "Hello"
            "You have received a barter trade offer. Check your dashboard for details."
        )
        status = "info"
        notification_repo.create_notification(user=product.seller, subject=subject, message=message, status=status,)

        phone = normalize_phone(str(product.seller.phone))
        send_sms_message(
            phone=phone,
            template="barter_trader.html",
            context={}
        )
        context = {
            "status": "success",
            "message": "Barter trader offer successfully sent",
            "data": None,
        }
        return ok, context
    return bad, {"status": "failed", "message": "Barter trade offer not sent", "data": None}
