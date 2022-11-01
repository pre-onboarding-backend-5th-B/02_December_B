import logging
import os

import pandas as pd
from django.core.management import BaseCommand

from company.models import StockCompany
from config.settings import BASE_DIR

"""
우선적으로 실행되어야 함
"""


class Command(BaseCommand):
    """
    asset_group_info_set.xlsx 파일을 읽어들여
    StockCompany 에 insert 한다.
    """
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        file_path = os.path.join(BASE_DIR, 'res', 'files', 'asset_group_info_set.xlsx')
        df = pd.read_excel(file_path)
        for row in df.itertuples():
            row_dict = row._asdict()
            di = {
                'name': row_dict.get('종목명'),
                'isin': row_dict.get('ISIN'),
                'group': row_dict.get('자산그룹'),
            }
            if not all(di.values()):  # None 값이 있으면 오류로 생각하고 넘긴다.
                continue
            try:
                if StockCompany.objects.filter(isin=di['isin']).exists():
                    continue
                scmpy = StockCompany(**di)
                scmpy.save()
            except Exception as e:
                logging.warning(e)
                pass
