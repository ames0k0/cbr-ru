import os.path
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
from decimal import Decimal, getcontext
from typing import TypeAlias

from config import const


__all__ = ['XML_daily']


getcontext().prec = const.DECIMAL_PREC
DATA_TYPE = dict[str, Decimal]


class XML_daily:
  # https://www.cbr.ru/scripts/XML_daily.asp?date_req=01/03/2002
  SCRIPT_NAME = 'XML_daily.asp'
  BASE_CURRENCY = 'rub'

  def __init__(self, date: str | None = None):
    BASE_URL = urllib.parse.urlparse(const.BASE_URL)

    self.SCRIPT_URL = urllib.parse.ParseResult(
      scheme=BASE_URL.scheme,
      netloc=BASE_URL.netloc,
      path='/'.join((
        os.path.split(os.path.dirname(__file__))[-1],
        self.SCRIPT_NAME
      )),
      query='' if not date else urllib.parse.urlencode({
        'date_req': date
      }),
      params='',
      fragment='',
    )
    self.SCRIPT_URL = urllib.parse.urlunparse(self.SCRIPT_URL)

  def convert_to_currency(
      self, target_currency: str, data: DATA_TYPE
  ) -> DATA_TYPE:
    """Converting the values to the `target_currency`

    Parameters
    ----------
    target_currency : str
      Converting the value with the `BASE_CURRENCY` to the `target_currency`
    data : dict[str, Decimal]
      Loaded data

    Raises
    ------
    ValueError
      `target_currency` not in the `data`'s `char_codes`

    Returns
    -------
    dict[str, Decimal]
      After convert will be added the `BASE_CURRENCY`
    """
    if target_currency not in data.keys():
      raise ValueError(f"{target_currency} not in the `data`")

    BASE = data.pop(target_currency)

    for char_code, value in data.items():
      data[char_code] = Decimal(BASE / value)

    data[self.BASE_CURRENCY] = BASE
    return data

  def load_data(
      self,
      char_codes: list[str] | None = None, ignore_missing: bool = False
  ) -> DATA_TYPE:
    """Loading the daily currency (or for specific `date`) for 1 `Nominal`

    Parameters
    ----------
    char_codes : list[str] | None
      Loading the data filtered by `char_codes` (LowerCased)
    ignore_missing : bool
      Ignoring missing filtered `char_codes`

    Raises
    ------
    ValueError
      Filtered data missing some `char_codes`

    Returns
    -------
    dict[str, Decimal] = {CharCode: Value}
    """
    data = {}
    response = urllib.request.urlopen(self.SCRIPT_URL).read()
    tree = ET.fromstring(response)

    for valute in tree:
      char_code = valute.find('CharCode').text.lower()

      if char_codes and char_code not in char_codes:
        continue

      nominal = int(valute.find('Nominal').text)
      value = valute.find('Value').text.replace(',', '.')

      data[char_code] = Decimal(value) / nominal

    if char_codes and not ignore_missing:
      missing_codes = set(char_codes) ^ set(data.keys())
      if missing_codes:
        raise ValueError(f"Missing char_codes: {missing_codes}")

    return data
