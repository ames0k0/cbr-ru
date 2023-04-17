
from scripts.XML_daily import XML_daily


xml_daily = XML_daily()
data = xml_daily.load_data(char_codes=['usd', 'cny'])
print('loaded data:', data)
data = xml_daily.convert_to_currency('usd', data)
print('converted data:', data)
