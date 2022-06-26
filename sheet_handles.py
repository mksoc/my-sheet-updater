import gspread


class SheetHandle():

  def __init__(self, sheet=None):
    self._gc = gspread.oauth()
    self.sheet = sheet

  @property
  def sheet(self):
    return self._sheet

  @sheet.setter
  def sheet(self, key):
    self._sheet = self._gc.open_by_key(key)
  