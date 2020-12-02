import requests
from bs4 import BeautifulSoup


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
  'FR0013534898': 'F0000162SO'
  }

  def price(self, isin):
    pricer = self._get_pricer(isin)
    return pricer(isin)

  def _get_pricer(self, isin):
    if isin in self._morningstar_dict:
      return self._get_morningstar
    else:
      raise ValueError(f'{isin} not found.')

  def _get_morningstar(self, isin):
    """
    Parse HTML of Morningstar fund page and extract the NAV
    """
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