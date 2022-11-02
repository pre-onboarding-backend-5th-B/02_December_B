from rest_framework.generics import ListAPIView, RetrieveAPIView

from .serializers import InvestmentListSerializer, InvestmentDetailSerializer

from .models import Account


class InvestmentListAPIView(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = InvestmentListSerializer


class InvestmentDetailAPIView(RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = InvestmentDetailSerializer
