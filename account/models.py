from django.core.validators import MinValueValidator
from django.db import models

from company.models import StockBroker


class Account(models.Model):
    """
    투자 계좌 모델
    """
    user = models.ForeignKey('user', on_delete=models.CASCADE)
    number = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=32)
    total_asset = models.IntegerField(validators=[MinValueValidator(0)],
                                      default=0)
    investment_principal = models.IntegerField(validators=[MinValueValidator(0)],
                                               default=0)
    stock_broker = models.ForeignKey(StockBroker, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.name}({self.number})'
