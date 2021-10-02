from bs4 import BeautifulSoup
import logging
import pandas as pd
import random
import requests
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

BASE_URL = 'http://www.politologue.com'
LIST_URL = f'{BASE_URL}/classement-interne-parti/'
RESULT_FILE_NAME = 'parties.csv'

def generate_parties():
  parties = _get_parties(LIST_URL)
  df = pd.DataFrame(columns=['name', 'party'])
  for name, link in parties.items():
    logging.info(f'Processing {name}')
    time.sleep(random.random())
    persons = _get_persons(f'{BASE_URL}{link}')
    df = df.append(pd.DataFrame({'name': persons, 'party': name}), ignore_index=True)
  logging.info(f'Printing results in {RESULT_FILE_NAME}')
  df.to_csv(RESULT_FILE_NAME)


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
  generate_parties()
