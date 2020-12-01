from abc import ABC, abstractmethod
import gspread


class BaseHandle(ABC):

  def __init__(self):
    self._gc = gspread.oauth()

  @property
  def sheet(self):
    return self._sheet

  @sheet.setter
  def sheet(self, key):
    self._sheet = self._gc.open_by_key(key)


class PortfolioHandle(BaseHandle):
  
  def __init__(self):
    super().__init__()
    print('Opening portfolio sheet...')
    self.sheet = '1uoIEzw7o0B9R5CRQMy_ki2V6dJ_d-c01cm7xkqn0n3Y'

  