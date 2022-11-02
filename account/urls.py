from django.urls import path

from .views import InvestmentListAPIView

urlpatterns = [
    path("investment/", InvestmentListAPIView.as_view(), name="investment-list"),
]
