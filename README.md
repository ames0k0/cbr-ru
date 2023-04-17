# cbr-ru: Банк России :: Технические ресурсы

```python
from scripts.XML_daily import XML_daily


xml_daily = XML_daily()

data = xml_daily.load_data(char_codes=['usd', 'cny'])
print('>>>', data)

data = xml_daily.convert_to_currency('usd', data)
print('<<<', data)


# >>> {'usd': Decimal('81.5045'), 'cny': Decimal('11.8803')}
# <<< {'cny': Decimal('6.86047'), 'rub': Decimal('81.5045')}
```
