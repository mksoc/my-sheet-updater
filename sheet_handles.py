import gspread


class BaseHandle():

  def __init__(self):
    self._gc = gspread.oauth()
    self._sheet = None

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

class NetWorthHandle(BaseHandle):
  
  def __init__(self):
    super().__init__()
    print('Opening net worth sheet...')
    self.sheet = '1bSKXlU59Hd4Lu8CVUCUScmOM854BlSEV1LRPxcOD2lg'

  