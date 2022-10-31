from django.core.validators import MinValueValidator
from django.db import models

from account.models import Account
from company.models import StockCompany


class Order(models.Model):
    """
    주문 내역
    """
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    stock_company = models.ForeignKey(StockCompany, on_delete=models.CASCADE)
    price = models.IntegerField(validators=[MinValueValidator(0)],
                                default=0,
                                help_text='주문 했을 당시 가격')
    amount = models.IntegerField(validators=[MinValueValidator(0)],
                                 default=0,
                                 help_text='주문한 주식 수')
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.account.name} ordered: {self.stock_company.name}' \
               f'({self.amount} x {self.price}) {self.ordered_at}'
