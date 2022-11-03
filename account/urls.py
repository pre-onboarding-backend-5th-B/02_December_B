from django.urls import path

from .views import InvestmentListAPIView, InvestmentDetailAPIView

urlpatterns = [
    path("investment/", InvestmentListAPIView.as_view(), name="investment-list"),
    path("investment/<int:pk>", InvestmentDetailAPIView.as_view(), name="investment-detail"),
]
