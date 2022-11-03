from django.core.validators import MinValueValidator
from django.db import models

from account.models import Account
from company.models import StockCompany


class Transfer(models.Model):
    """
    주문 내역
    """
    PENDING = 'P'
    SUCCESS = 'S'
    TRANSFER_STATUS = [
        (PENDING, 'pending'),  # phase 1 을 통과했으나, 송금이 완료된 상태는 아님
        (SUCCESS, 'success'),  # phase 2 까지 통과하여 송금이 성공한 상태
    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    price = models.IntegerField(validators=[MinValueValidator(100)],
                                help_text='송금은 최소 100원 이상을 보내주세요')
    status = models.CharField(
        max_length=1,
        choices=TRANSFER_STATUS,
        help_text='송금 상태를 넣어 주세요.'
    )
    transfer_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.account.user_name}/{self.account.number} {self.price} {self.transfer_at}'
