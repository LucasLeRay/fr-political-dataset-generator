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
)
from exceptions import NoMoreSpeech, TooMuchSpeaker, UnknownSpeaker


def generate_speeches(begin_page=0, end_page=None):
  page = begin_page
  parties_df = pd.read_csv(PARTIES_FILE_PATH)
  parties_df.set_index('name', inplace=True)

  while True:
    logging.info(f'Processing page {page}')
    try:
      links = get_speeches_links(f'{SPEECHES_LIST_URL}?page={page}')
      if end_page is not None and page >= end_page:
        break
    except NoMoreSpeech:
      break
    for link in links:
      try:
        speech = get_speech(f'{SPEECHES_BASE_URL}{link}', parties_df)
        write_file(**speech, link=link, path=SPEECHES_FOLDER_PATH)
      except (TooMuchSpeaker, UnknownSpeaker):
        pass
    page += 1


def write_file(speaker, party, content, year, link, path):
  folder = f'{path}/{party}/{year}/{speaker}'
  os.makedirs(folder, exist_ok=True)
  file_name = link.split('/')[-1]
  with open(f'{folder}/{file_name}', 'w+') as f:
    f.write(content)


def get_speeches_links(url):
  res = requests.get(url)
  soup = BeautifulSoup(res.content, features="lxml")
  if no_more_speeches(soup):
    raise NoMoreSpeech()
  return list(link['about'] for link in soup.find_all('div', {'role': 'article'}))


def no_more_speeches(soup):
  return soup.find('div', {'class': 'view-empty'}) is not None


def get_speech(url, parties_df):
  res = requests.get(url)
  soup = BeautifulSoup(res.content, features="lxml")
  speaker = get_speech_speaker(soup)
  return {
    'speaker': speaker,
    'party': get_political_party(speaker, parties_df),
    'content': get_speech_content(soup),
    'year': get_speech_year(soup),
  }


def get_speech_content(soup):
  speech = soup.find('span', {'class': 'field--name-field-texte-integral'})
  # Sometimes sources can be added at the end of the speech
  return re.sub(r"Source http.*\n", '', speech.text).strip()


def get_speech_speaker(soup):
  speakers_wrapper = soup.find('ul', {'class': 'line-intervenant'})
  speakers = speakers_wrapper.find_all('li')
  if len(speakers) > 1:
    raise TooMuchSpeaker()
  return speakers[0].find('a').text.strip()


def get_speech_year(soup):
  date = soup.find('span', {'class': 'field--name-field-date-prononciation-discour'})
  return date.text.split(' ')[-1].strip()


def get_political_party(name, df):
  try:
    return df.loc[name]['party']
  except KeyError:
    raise UnknownSpeaker(name)


if __name__ == '__main__':
  generate_speeches(0, 500)
