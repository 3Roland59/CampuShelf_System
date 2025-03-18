from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from products.serializers import ProductSerializer
from products.repository import (
    ProductRepository,
    ProductImageRepository,
)

product_repo = ProductRepository
product_image_repo = ProductImageRepository


def add_product(request: Request, serializer_class: ProductSerializer, **kwargs):
    ok = HTTP_200_OK
    bad = HTTP_400_BAD_REQUEST
    data = request.data
    serializer = serializer_class(data=data)
    if serializer.is_valid(raise_exception=True):
        images_data = request.FILES.getlist("product_images")
        # print(type(images_data))
        # print("list of imges", images_data)
        # create product after checks
        product = serializer.save(seller=request.user)

        # product images
        for image_data in images_data:
            print(images_data)
            product_image_repo.create_product_image(
                product=product,
                image=image_data
            )

        context = {
            "status": "success",
            "message": "Product added successfully",
            "data": serializer.data,
        }
        return ok, context

    return bad, {
        "status": "failed",
        "message": "Product was not added",
        "details": serializer.errors,
    }


def get_products(request: Request, serializer_class: ProductSerializer, **kwargs):
    ok = HTTP_200_OK
    products = product_repo.get_all_products()
    serializer = serializer_class(products, many=True)
    context = {"status": "success", "message": "All products", "data": serializer.data}
    return ok, context


def get_products_by_category(
    request: Request,
    serializer_class: ProductSerializer,
    category_id,
):
    ok = HTTP_200_OK
    products = product_repo.get_all_products_by_category(
        category_id=category_id,
    )
    if products:
        serializer = serializer_class(products, many=True)
        context = {
            "status": "success",
            "message": "All category products",
            "data": serializer.data,
        }
        return ok, context
    else:
        context = {
            "status": "success",
            "message": "All category products",
            "data": None,
        }
        return ok, context
