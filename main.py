import config
from datetime import datetime
from sheet_handles import SheetHandle
from quotation_parser import QuotationParser
import json
import requests
from bs4 import BeautifulSoup

options = {
    '1': 'update_au',
    '2': 'update_portfolio',
    'a': 'all',
    'q': 'quit'
}

def print_with_time(string):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'({timestamp}) {string}')

def print_menu():
    print()
    print('Available options:')
    for key in options:
        print(f'{key}: {options[key]}')
    print()

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

def update_portfolio():
    try:
        with open(config.portfolio, 'r') as portfolio_file:
            pass
    except FileNotFoundError as e:
        print(f'Error: {e}')
        print('Could not complete portfolio update, check that the Excel file is there.')
        return

def all():
    update_au()
    update_portfolio()

def quit():
    print('Goodbye.')
    exit()

if __name__ == '__main__':
    while(True):
        print_menu()
        choice = input('Please enter your choice: ')
        
        if choice in options.keys():
            eval(options[choice] + '()')
        else:
            print('Invalid option. Please try again.')