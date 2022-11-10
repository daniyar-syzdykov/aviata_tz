from xml.etree import ElementTree as et
from api.exchange_cache import EXCHANGE_CAHCE

def save_conversion_reate(raw_xml):
    exchange_rate = {}
    root = et.fromstring(raw_xml)
    for e in root.iter('item'):
        title = e.find('title').text
        exchange_rate.update({
            title: {
                'quant': e.find('quant').text,
                'description': e.find('description').text
            }
        })
    exchange_rate.update({'KZT': {'quant': 1, 'description': 1}})
    EXCHANGE_CAHCE.update(exchange_rate)


def get_exchange_rate(currency):
    return EXCHANGE_CAHCE.get(currency)


def convert(from_currency, to_currency, old_price):
    exchange_rate = get_exchange_rate(from_currency)
    quant = exchange_rate.get('quant')
    description = exchange_rate.get('description')
    return float(old_price) * float(description) / float(quant)


async def convert_result_curency(search_results, currency):
    for results in search_results.get('details'):
        result_currency = results.get('currency')
        price = results.get('price')
        converted_price = convert(
            from_currency=result_currency, to_currency=currency, old_price=price)
        results.update({
            'price': {
                'amount': converted_price,
                'currency': currency
            }
        })
    return search_results
