from django.core.validators import MinValueValidator
from django.db import models

from account.models import Account
from company.models import StockCompany


class Portfolio(models.Model):
    """
    보유 종목
    """
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    


class PortfolioLog(models.Model):
    """
    종목별 매수 기록
    """
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock_company = models.ForeignKey(StockCompany, on_delete=models.CASCADE)
    price = models.IntegerField(validators=[MinValueValidator(0)],
                                default=0,
                                help_text='매수 당시 가격')
    amount = models.IntegerField(validators=[MinValueValidator(0)],
                                 default=0,
                                 help_text='보유 주식 수')
    file_mtime_hashing = models.CharField(max_length=256,
                                          blank=True,
                                          null=True,
                                          help_text='파일 업로드 된 시간을 비교하여 데이터를 덮어씌울지, 추가시킬지 판단함')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
