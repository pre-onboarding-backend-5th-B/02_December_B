import hashlib

from account.models import Account


def get_hashing(account: Account, price: str) -> str:
    code = f'{account.number}{account.user_name}{price}'
    b_code = bytes(code, 'utf-8')
    return hashlib.sha256(b_code).hexdigest()