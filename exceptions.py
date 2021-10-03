class TooMuchSpeaker(Exception):
  pass

class UnknownSpeaker(Exception):
  pass

class NoMoreSpeech(Exception):
  pass

class PartiesFileNotFound(FileNotFoundError):
  def __init__(self, message):
    super().__init__(f'Parties file not found at "{message}", did you generate it?')
