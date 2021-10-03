import logging
import os

import click

from constants import LOGGING_FORMAT, PARTIES_FILE_PATH
from exceptions import PartiesFileNotFound
from generate_parties import generate_parties
from generate_speeches import generate_speeches


def handle_verbose(verbose):
  if not verbose:
    logging.disable()
  else:
    logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)


def shared_options(func):
  options = [
    click.option("--verbose", type=bool, default=True, help="Default false")
  ]
  for option in options:
    func = option(func)

  return func


@click.group()
def cli():
  pass


@cli.command()
@shared_options
def parties(verbose):
  handle_verbose(verbose)
  generate_parties()


@cli.command()
@shared_options
@click.option("--from-page", type=int, default=0, help="Page to start from. Start at 0 (inclusive)")
@click.option("--to-page", type=int, default=None, help="Page to end at (exclusive). Default stops when there are no more speeches.")
@click.option("--create-parties", is_flag=True, help="Create parties file directly")
def speeches(verbose, from_page, to_page, create_parties):
  handle_verbose(verbose)
  if create_parties:
    generate_parties()
  if not os.path.exists(PARTIES_FILE_PATH):
    raise PartiesFileNotFound(PARTIES_FILE_PATH)
  generate_speeches(from_page=from_page, to_page=to_page)


if __name__ == '__main__':
  cli()
