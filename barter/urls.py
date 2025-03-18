from django.urls import path
from barter.views import BarterCreateView

urlpatterns = [
    path(
        "barter-trade/",
        BarterCreateView.as_view(),
        name="barter-trade",
    ),
]
