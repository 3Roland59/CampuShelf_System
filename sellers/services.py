from products.repository import ProductRepository

from rest_framework.status import HTTP_200_OK

product_repo = ProductRepository


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
