import json
import requests
from config import keys, YOUR_API_KEY


class ConvertionException(Exception):
    pass


class CurrenciesConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        conv_ticker = f'{quote_ticker}_{base_ticker}'
        r = requests.get(
            f'https://free.currconv.com/api/v7/convert?q={conv_ticker}&compact=ultra&apiKey={YOUR_API_KEY}')
        total_base = round(json.loads(r.content)[conv_ticker] * amount, 4)
        return total_base
