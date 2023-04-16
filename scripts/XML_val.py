# script: XML_val.asp

import os
from pathlib import Path

from config import const


class XML_val:
  # https://www.cbr.ru/scripts/XML_val.asp?d=0
  SCRIPT_URL = f"{const.BASE_URL}/XML_val.asp?d0"
  SCRIPT_NAME = 'XML_val.asp'
  BASE_URL = os.path.join(
    const.BASE_URL,
    os.path.split(os.path.dirname(__file__))[-1],
    SCRIPT_NAME
  )
  print(BASE_URL)
