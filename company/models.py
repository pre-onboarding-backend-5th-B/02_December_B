from django.core.validators import MinValueValidator
from django.db import models


class Group(models.Model):
    """
    투자 그룹 섹터
    """
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class StockBroker(models.Model):
    """
    증권사
    """
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class StockCompany(models.Model):
    """
    주식 회사(투자할 회사)
    """
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    price = models.IntegerField(validators=[MinValueValidator(0)],
                                default=0,
                                help_text='현재 주가')
    amount = models.IntegerField(validators=[MinValueValidator(0)],
                                 default=0,
                                 help_text='주식 발행량 수')

    def __str__(self):
        return f'{self.name}({self.group.name})'
