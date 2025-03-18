from products.repository import ProductRepository
from barter.repository import BarterRepository

from rest_framework.status import HTTP_200_OK

product_repo = ProductRepository
barter_repo = BarterRepository


def get_user_products(request, serializer_class):
    ok = HTTP_200_OK
    user = request.user
    products = product_repo.get_user_products(seller=user)
    data = serializer_class(products, many=True).data
    context = {
        "status": "success",
        "message": "User Products",
        "data": data,
    }
    return ok, context


def get_user_barter(request, serializer_class):
    ok = HTTP_200_OK
    user = request.user
    barters = barter_repo.get_user_barter(seller=user)
    data = serializer_class(barters, many=True).data
    context = {
        "status": "success",
        "message": "User Barter Offers",
        "data": data,
    }
    return ok, context
