import logging
import os

import pandas as pd
from django.core.management import BaseCommand

from account.models import Account
from config.settings import BASE_DIR

"""
insert assets 커맨드가 미리 실행된다고 가정한다.
왜냐하면 account 에는 stock_broker 필드가 생성되어야 하는데
basic xlsx 파일에는 stock_broker 가 없음
"""


class Command(BaseCommand):
    """
    account_basic_info_set.xlsx 파일을 읽어들여
    Account Model에 계좌번호로 투자원금을 update 함
    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        file_path = os.path.join(BASE_DIR, 'res', 'files', 'account_basic_info_set.xlsx')
        df = pd.read_excel(file_path)
        for row in df.itertuples():
            row_dict = row._asdict()
            number = row_dict.get('계좌번호')
            investment_principal = row_dict.get('투자원금')
            if None in [number, investment_principal]:
                continue
            try:
                Account.objects.update_or_create(
                    number=number,
                    defaults={'investment_principal': investment_principal}
                )
            except Exception as e:
                logging.warning(e)
                continue
