from django.core.validators import MinValueValidator
from django.db import models


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
    isin = models.CharField(max_length=64)
    group = models.CharField(max_length=64)
    name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.name}/{self.isin}/{self.group}'
