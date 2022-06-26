import config
from datetime import datetime
from sheet_handles import SheetHandle
from quotation_parser import QuotationParser
import json
import requests
from bs4 import BeautifulSoup


def print_with_time(string):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'({timestamp}) {string}')

def update_au():
    handle = SheetHandle(config.au_sheet)
    parser = QuotationParser()
    print_with_time('Updating Au sheet...')

    # Write the date
    print('\tWriting quotation date...')
    current_sheet = handle.sheet.get_worksheet(0)
    date = parser.get_date()
    current_sheet.update('B28', f'{date.day}/{date.month}/{date.year}')

    # Update prices
    print('\tWriting prices...')
    with open(config.au_json) as json_file:
        au_dict = json.load(json_file)

    total = len(au_dict.items())
    for index, (key, value) in enumerate(au_dict.items()):
        price = parser.get_price(value)
        print(f'\t\t({index+1:2}/{total}) {key}: {price:.2f}€')
        current_sheet.update(value['cell'], price)

    # Get unit price
    print('\tUpdating spot price...')
    current_sheet = handle.sheet.get_worksheet(1)
    page = requests.get(config.price_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    price = soup.find_all('font', class_='ValoreQuotazione')[1].text
    current_sheet.update('F2', float(price.split()[0]))

    print_with_time('Done updating Au sheet.')

if __name__ == '__main__':
    update_au()