import os
import pandas as pd

from config.settings import BASE_DIR


def read_xlsx(file_nm: str) -> dict:
    """

    :param file_nm: 파일 경로는 정해져 있다고 생각하고 파일 이름만 넣으면 된다고 가정
    :return: iterator
    """
    file_path = os.path.join(BASE_DIR, 'res', 'files', file_nm)
    df = pd.read_excel(file_path)
    length = len(df)
    for i, row in enumerate(df.itertuples(), 1):
        print(f'{i} / {length} ...')
        yield row._asdict()