import datetime
import requests


def get_currency(base: str = 'RUB', convert: str = 'USD') -> dict[str, any]:

    request = requests.get("https://www.cbr-xml-daily.ru/latest.js").json()

    return {
        'base': request.get('base') or base,
        'convert': convert,
        'rate': request.get('rates').get('USD'),
        'datetime': datetime.datetime.now()
    }

