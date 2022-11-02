from django.urls import path

from .views import InvestmentAPIView

urlpatterns = [
    path('investment', InvestmentAPIView.as_view(), name='investment-list'),
]
