import logging
import os

from constants import (
  DEFAULT_PATH,
  LOGGING_FORMAT,
)

os.makedirs(DEFAULT_PATH, exist_ok=True)

logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)
