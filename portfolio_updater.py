from sheet_handles import PortfolioHandle
import requests
from bs4 import BeautifulSoup


def get_nav(id):
  """
  Parse HTML of Morningstar fund page and extract the NAV
  """
  url = f'https://www.morningstar.it/it/funds/snapshot/snapshot.aspx?id={id}'
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  overview_table = soup.find(id='overviewQuickstatsDiv')
  titles = overview_table.find_all('td', class_='line heading')
  text = overview_table.find_all('td', class_='line text')
  index = [idx for idx, s in enumerate(titles) if 'NAV' in s][0]
  nav = str(text[index]).split('EUR')[-1].split('<')[0].strip().replace(',', '.')
  return round(float(nav), 2)


# Create handle to Google Sheet and find column to update
portfolio = PortfolioHandle()
ws = portfolio.sheet.get_worksheet(1)
col_idx = ws.find('Prezzo di mercato').col

# Define dictionary of ISIN
isin_dict = {
  'LU0552385295': '0P0000RZ2Q',
  'LU0594300096': 'F00000M0N7',
  'LU0171306680': 'F000014TUF',
  'IE00B11XZ103': 'F0GBR06T61',
  'LU0512749036': 'F00000IRWU',
  'LU0849399786': 'F00000P15I',
  'FR0010923383': 'F000015UA4',
  'FR0013534898': 'F0000162SO'
}
items = len(isin_dict)

# For each entry, retrieve NAV and update sheet
for index, (key, value) in enumerate(isin_dict.items()):
  print(f'({index + 1}/{items}) Updating NAV of {key}...', end=' ', flush=True)
  row_idx = ws.find(key).row
  nav = get_nav(value)
  print(f'€{nav:.2f}')
  ws.update_cell(row_idx, col_idx, nav)

print('Done.')