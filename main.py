
from scripts.XML_daily import XML_daily


xml_daily = XML_daily()
data = xml_daily.load_data(char_codes=['usd', 'cny'])
print('>>>', data)
data = xml_daily.convert_to_currency('usd', data)
print('<<<', data)
