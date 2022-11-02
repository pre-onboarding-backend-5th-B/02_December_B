import logging

from rest_framework import viewsets, status
from rest_framework.response import Response

from account.models import Account
from transfer.models import Transfer
from transfer.serializers import TransferSerializer, TransferDetailSerializer
from transfer.utils import get_hashing


# Create your views here.
class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer

    def create(self, request, *args, **kwargs):
        # phase 1 을 판단
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        try:
            account = Account.objects.get(pk=request.POST.get('account'))
        except Exception as e:
            logging.warning(e)
            return Response({'message': '계좌 id 를 확인하세요.'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            price = request.POST.get('price')
            hashing = get_hashing(account, price)
            transfer_id = serializer.data['id']
            message = {
                'signature': hashing,
                'transfer_id': transfer_id
            }
            return Response(message, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        # phase 2 를 진행함 pending 에서 success 로 바꾸므로 update 라고 판단
        request_sig = request.POST.get('signature')
        queryset = Transfer.objects.get(pk=kwargs['pk'])
        server_sig = get_hashing(queryset.account, queryset.price)
        if request_sig == server_sig:
            queryset.status = Transfer.SUCCESS
            return Response({'status': queryset.status}, status=status.HTTP_200_OK)
        return Response({'message': 'Does not match'}, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update']:
            return TransferDetailSerializer
        return TransferSerializer
