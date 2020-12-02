#!/usr/bin/python3

from sheet_handles import PortfolioHandle
from price_getter import PriceGetter
from datetime import datetime

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
  count = f'({index + 1}/{items})'
  print(f'{count: <7}', end=' ', flush=True)
  row_idx = ws.find(isin).row
  price = pg.price(isin)
  print_price(isin, price)
  ws.update_cell(row_idx, col_idx, price)

# Write datetime of update
update_cell = ws.find('Ultimo aggiornamento:')
col_idx = update_cell.col + 1
row_idx = update_cell.row
now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
ws.update_cell(row_idx, col_idx, now)

print('Done.')