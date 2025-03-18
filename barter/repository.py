from barter.models import Barter


class BarterRepository:
    model = Barter.objects

    @classmethod
    def get_user_barter(cls, seller=None):
        barter = cls.model.filter(seller=seller)
        return barter
