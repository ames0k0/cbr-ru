# script: XML_daily.asp

import os
import datetime as dt

from config import const


# from urllib.urlopen import urlopen

import xml.etree.ElementTree as ET
import urllib.request


from decimal import Decimal, getcontext

getcontext().prec = 4


class XML_daily:
  # https://www.cbr.ru/scripts/XML_daily.asp?date_req=02/03/2002
  SCRIPT_LOC = os.path.split(os.path.dirname(__file__))[-1]
  SCRIPT_NAME = 'XML_daily.asp'
  SCRIPT_URL = f"{const.BASE_URL}/{SCRIPT_LOC}/{SCRIPT_NAME}"


##
data = {}
response = urllib.request.urlopen(XML_daily.SCRIPT_URL).read()


tree = ET.fromstring(response)
for valute in tree:
  char_code = valute.find('CharCode').text

  if char_code not in ('USD', 'CNY', 'EUR'):
    continue

  nominal = int(valute.find('Nominal').text)
  value = valute.find('Value').text.replace(',', '.')

  data[char_code] = Decimal(value) / nominal
  # print(char_code)
  # print(nominal)
  # print(char_code, '>', value, '::', nominal)


def convert_to_base(base_char_code, data):
  BASE = data.pop(base_char_code)
  for k, v in data.items():
    data[k] = float(Decimal(BASE / v))
  return data


data = convert_to_base('USD', data)


print(data)


# a = {"cny":"6.8688","eur":"0.909200","rub":"82.26"}
# b = {'EUR': Decimal('1.10624'), 'CNY': Decimal('0.145763')}
# c = {'EUR': Decimal('0.903961'), 'CNY': Decimal('6.86047')}
