import logging
import os
import re

from bs4 import BeautifulSoup
import pandas as pd
import requests

import config
from constants import (
  SPEECHES_BASE_URL,
  SPEECHES_LIST_URL,
  PARTIES_FILE_PATH,
  SPEECHES_FOLDER_PATH,
  NAME_COLUMN,
  PARTY_COLUMN,
)
from exceptions import NoMoreSpeech, TooMuchSpeaker, UnknownSpeaker


def generate_speeches(*, from_page=0, to_page=None):
  page = from_page
  parties_df = pd.read_csv(PARTIES_FILE_PATH)
  parties_df.set_index(NAME_COLUMN, inplace=True)

  while True:
    if to_page is not None and page >= to_page:
      break
    logging.info(f'Processing page {page}')
    try:
      links = _get_speeches_links(f'{SPEECHES_LIST_URL}?page={page}')
    except NoMoreSpeech:
      break
    for link in links:
      try:
        speech = _get_speech(f'{SPEECHES_BASE_URL}{link}', parties_df)
        _write_file(**speech, link=link, path=SPEECHES_FOLDER_PATH)
      except (TooMuchSpeaker, UnknownSpeaker):
        pass
      except Exception as e:
        logging.error(e)
        pass
    page += 1


def _write_file(speaker, party, content, year, link, path):
  folder = f'{path}/{party}/{year}/{speaker}'
  os.makedirs(folder, exist_ok=True)
  file_name = link.split('/')[-1]

  with open(f'{folder}/{file_name}', 'w+') as f:
    f.write(content)


def _get_speeches_links(url):
  res = requests.get(url)
  soup = BeautifulSoup(res.content, features="lxml")

  if _no_more_speeches(soup):
    raise NoMoreSpeech()

  return list(link['about'] for link in soup.find_all('div', {'role': 'article'}))


def _no_more_speeches(soup):
  return soup.find('div', {'class': 'view-empty'}) is not None


def _get_speech(url, parties_df):
  res = requests.get(url)
  soup = BeautifulSoup(res.content, features="lxml")
  speaker = _get_speech_speaker(soup)

  return {
    'speaker': speaker,
    'party': _get_political_party(speaker, parties_df),
    'content': _get_speech_content(soup),
    'year': _get_speech_year(soup),
  }


def _get_speech_content(soup):
  speech = soup.find('span', {'class': 'field--name-field-texte-integral'})
  # Sometimes sources can be added at the end of the speech
  return re.sub(r"(Source|source) http.*\n", '', speech.text).strip()


def _get_speech_speaker(soup):
  speakers_wrapper = soup.find('ul', {'class': 'line-intervenant'})
  speakers = speakers_wrapper.find_all('li')

  if len(speakers) > 1:
    raise TooMuchSpeaker()

  return speakers[0].find('a').text.strip()


def _get_speech_year(soup):
  date = soup.find('span', {'class': 'field--name-field-date-prononciation-discour'})

  return date.text.split(' ')[-1].strip()


def _get_political_party(name, df):
  try:
    return df.loc[name][PARTY_COLUMN]
  except KeyError:
    raise UnknownSpeaker(name)


if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  generate_speeches(from_page=0, to_page=1)
