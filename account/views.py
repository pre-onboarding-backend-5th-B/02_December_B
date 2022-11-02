from rest_framework.generics import ListAPIView

from .serializers import InvestmentListSerializer

from .models import Account


class InvestmentListAPIView(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = InvestmentListSerializer
