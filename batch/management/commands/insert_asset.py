import logging
import os
from collections import namedtuple

import pandas as pd
from django.core.management import BaseCommand

from account.models import Account
from company.models import StockBroker, StockCompany
from config.settings import BASE_DIR
from portfolio.models import PortfolioLog, Portfolio

"""
insert company 가 먼저 선행되서 실행되어야 함
"""


# namedtuple 자료형 검사
def isinstance_namedtuple(obj) -> bool:
    return (
            isinstance(obj, tuple) and
            hasattr(obj, '_asdict') and
            hasattr(obj, '_fields')
    )


class Command(BaseCommand):
    """
    account_assets_info.xlsx 를 읽어 들여서
    Account, StockBroker, StockCompany, Portfolio, PortfolioLog 에 insert 한다.
    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        file_path = os.path.join(BASE_DIR, 'res', 'files', 'account_asset_info_set.xlsx')
        df = pd.read_excel(file_path)
        xlsx2model = namedtuple('Convert', 'model dataset')
        for row in df.itertuples():
            try:
                row_dict = row._asdict()
                stock_broker = {'name': row_dict.get('증권사')}
                stock_company = {'isin': row_dict.get('ISIN')}
                account = {
                    'user_name': row_dict.get('고객이름'),
                    'number': row_dict.get('계좌번호'),
                    'name': row_dict.get('계좌명'),
                    'stock_broker': StockBroker.objects.get_or_create(**stock_broker)[0]
                }
                portfolio = {
                    'account': Account.objects.get_or_create(**account)[0],
                    'stock_company': StockCompany.objects.get_or_create(**stock_company)[0],
                }
                portfolio_log = {
                    'portfolio': Portfolio.objects.get_or_create(**portfolio)[0],
                    'price': row_dict.get('현재가'),
                    'amount': row_dict.get('보유수량')
                }
            except Exception as e:
                logging.warning(e)
                continue
            else:
                dataset = [xlsx2model(model=StockBroker, dataset=stock_broker),
                           xlsx2model(model=StockCompany, dataset=stock_company),
                           xlsx2model(model=Account, dataset=account),
                           xlsx2model(model=Portfolio, dataset=portfolio),
                           xlsx2model(model=PortfolioLog, dataset=portfolio_log)]

                for x in dataset:
                    if x.model.objects.filter(**x.dataset).exists():
                        continue
                    try:
                        instance = x.model(**x.dataset)
                        instance.save()
                    except Exception as e:
                        logging.warning(e)
                        continue
