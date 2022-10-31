from django.core.validators import MinValueValidator
from django.db import models

from account.models import Account
from company.models import StockCompany


class Portfolio(models.Model):
    """
    보유 종목
    """
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    stock_company = models.ForeignKey(StockCompany, on_delete=models.CASCADE)


class PortfolioLog(models.Model):
    """
    종목별 매수 기록
    """
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    price = models.IntegerField(validators=[MinValueValidator(0)],
                                default=0,
                                help_text='매수 당시 가격')
    amount = models.IntegerField(validators=[MinValueValidator(0)],
                                 default=0,
                                 help_text='보유 주식 수')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
