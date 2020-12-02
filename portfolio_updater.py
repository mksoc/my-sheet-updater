from sheet_handles import PortfolioHandle
from price_getter import PriceGetter

def print_price(isin, price):
  if 'US' in isin:
    print(f'\t${price:.2f}')
  else:
    print(f'\t€{price:.2f}')

# Create handle to Google Sheet and find column to update
# pylint: disable=E1101
portfolio = PortfolioHandle()
ws = portfolio.sheet.get_worksheet(1)
col_idx = ws.find('Prezzo di mercato').col

# Create PriceGetter instance
pg = PriceGetter()

# Define list of ISIN to update
isin_list = [
  'LU0552385295',
  'LU0594300096',
  'US69608A1088',
  'LU0171306680',
  'IE00B11XZ103',
  'IE00BK5BQT80',
  'LU0512749036',
  'LU0849399786',
  'FR0010923383',
  'FR0013534898',
  'IT0005410904'
]
items = len(isin_list)


# For each entry, retrieve NAV and update sheet
for index, isin in enumerate(isin_list):
  print(f'({index + 1}/{items})', end=' ', flush=True)
  row_idx = ws.find(isin).row
  price = pg.price(isin)
  print_price(isin, price)
  ws.update_cell(row_idx, col_idx, price)

print('Done.')