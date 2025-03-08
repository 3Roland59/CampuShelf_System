from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from buyers.repository import BuyerSavedProductRepo, BuyerCartRepo
from products.repository import ProductRepository
from rest_framework.request import Request


buyer_sp_repo = BuyerSavedProductRepo
product_repo = ProductRepository
buyer_cart_repo = BuyerCartRepo


def get_buyer_saved_products(request: Request, serializer_class, *args, **kwargs):
    ok = HTTP_200_OK
    buyer = request.user
    products = buyer_sp_repo.get_buyer_saved_products(buyer=buyer)
    serializer = serializer_class(products, many=True)
    return ok, {
        "status": "success",
        "message": "Buyer Saved Products",
        "data": serializer.data,
    }


def delete_saved_product(request: Request, product_id):
    ok = HTTP_200_OK
    not_found = HTTP_404_NOT_FOUND
    user = request.user
    product = product_repo.get_product_by_id(product_id=product_id)
    if product is None:
        return not_found, {
            "status": "error",
            "message": "Product does not exist",
        }
    buyer_saved = buyer_sp_repo.get_buyer_saved(buyer=user)
    buyer_saved.products.remove(product)

    context = {
        "status": "Success",
        "message": "Product deleted from saved",
    }
    return ok, context


def get_buyer_cart_products(request: Request, serializer_class, *args, **kwargs):
    ok = HTTP_200_OK
    buyer = request.user
    products = buyer_cart_repo.get_buyer_cart_products(buyer=buyer)
    serializer = serializer_class(products, many=True)
    return ok, {
        "status": "success",
        "message": "Buyer Cart Products",
        "data": serializer.data,
    }


def delete_cart_product(request: Request, product_id):
    ok = HTTP_200_OK
    not_found = HTTP_404_NOT_FOUND
    user = request.user
    product = product_repo.get_product_by_id(product_id=product_id)
    if product is None:
        return not_found, {
            "status": "error",
            "message": "Product does not exist",
        }
    buyer_cart = buyer_cart_repo.get_buyer_cart(buyer=user)
    buyer_cart.products.remove(product)

    context = {
        "status": "Success",
        "message": "Product deleted from cart",
    }
    return ok, context
