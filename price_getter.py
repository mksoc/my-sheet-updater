import requests
from bs4 import BeautifulSoup
import re
from yahoo_fin import stock_info


class PriceGetter:
  """
  Get stock, bond and fund prices from different sources.
  """
  
  _morningstar_dict = {
    'LU0552385295': '0P0000RZ2Q',
    'LU0594300096': 'F00000M0N7',
    'LU0171306680': 'F000014TUF',
    'IE00B11XZ103': 'F0GBR06T61',
    'LU0512749036': 'F00000IRWU',
    'LU0849399786': 'F00000P15I',
    'FR0010923383': 'F000015UA4',
    'FR0013535077': 'F0000162SP'
  }

  _aff_dict = {
    'IT0005410904': 'obbligazioni/mot/btp/scheda/IT0005410912',
    'IE00BK5BQT80': 'etf/scheda/IE00BK5BQT80'}

  _nyse_dict = {
    'US69608A1088': 'PLTR'
  }

  def price(self, isin):
    pricer = self._get_pricer(isin)
    return pricer(isin)

  def _get_pricer(self, isin):
    if isin in self._morningstar_dict:
      return self._get_morningstar
    elif isin in self._aff_dict:
      return self._get_aff
    elif isin in self._nyse_dict:
      return self._get_nyse
    else:
      raise ValueError(f'{isin} not found.')

  def _get_morningstar(self, isin):
    """
    Parse HTML of Morningstar fund page and extract the NAV
    """
    print(f'Looking up price of {isin} on Morningstar...')
    morningstar_id = self._morningstar_dict[isin]
    url = f'https://www.morningstar.it/it/funds/snapshot/snapshot.aspx?id={morningstar_id}'
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    overview_table = soup.find(id='overviewQuickstatsDiv')
    titles = overview_table.find_all('td', class_='line heading')
    text = overview_table.find_all('td', class_='line text')
    index = [idx for idx, s in enumerate(titles) if 'NAV' in s][0]
    nav = str(text[index]).split('EUR')[-1].split('<')[0].strip().replace(',', '.')
    return round(float(nav), 2)

  def _get_aff(self, isin):
    """
    Parse HTML of Borsa Italiana page and extract the price
    """
    print(f'Looking up price of {isin} on Borsa Italiana...')
    aff_path = self._aff_dict[isin]
    url = f'https://www.borsaitaliana.it/borsa/{aff_path}.html?lang=it'
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    # pylint: disable=W1401
    table_div = soup.find('h3', string=re.compile('Dati Mercato\s')).parent.parent
    table = table_div.find('table', class_="m-table -clear-mtop")
    price_row = table.find('tr')
    price = price_row.find('span', class_="t-text -right").string.replace(',', '.')
    return round(float(price), 2)

  def _get_nyse(self, isin):
    """
    Parse HTML of NYSE page and extract the price
    """
    print(f'Looking up price of {isin} on NYSE...')
    ticker = self._nyse_dict[isin]
    price = stock_info.get_live_price(ticker)
    return round(float(price), 2)