from rest_framework.generics import ListAPIView

from .models import Account


class InvestmentListAPIView(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = InvestmentListSerializer
