from reviews.models import ProductReview


class ProductReviewRepository:
    model = ProductReview.objects

    @classmethod
    def get_reviews(cls, product_id):
        try:
            reviews = cls.model.filter(product=product_id)
        except:
            ...
        else:
            return reviews
