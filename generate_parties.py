import logging
import random
import time

from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib3

import config
from constants import (
  PARTIES_BASE_URL,
  PARTIES_LIST_URL,
  PARTIES_FILE_PATH,
  NAME_COLUMN,
  PARTY_COLUMN
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def generate_parties():
  parties = _get_parties(PARTIES_LIST_URL)
  df = pd.DataFrame(columns=[NAME_COLUMN, PARTY_COLUMN])

  for name, link in parties.items():
    logging.info(f'Processing {name}')
    time.sleep(random.random())
    persons = _get_persons(f'{PARTIES_BASE_URL}{link}')
    df = df.append(pd.DataFrame({NAME_COLUMN: persons, PARTY_COLUMN: name}), ignore_index=True)

  logging.info(f'Printing results in {PARTIES_FILE_PATH}')
  df.set_index(NAME_COLUMN, inplace=True)
  df.to_csv(PARTIES_FILE_PATH)


def _get_parties(url):
  parties = {}
  page = requests.get(url, verify=False)
  soup = BeautifulSoup(page.content, 'html.parser')
  table = soup.find('table', class_='table-classement')

  for party_elem in table.findChildren("tr" , recursive=False):
    parties[party_elem.find('a')['title']] = party_elem.find('a')['href']

  return parties


def _get_persons(url):
  party_page = requests.get(url, verify=False)
  soup = BeautifulSoup(party_page.content, 'html.parser')
  table = soup.find('table', class_='table-classement')

  return list(name.text for name in table.find_all('a', class_='bold'))


if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  generate_parties()
