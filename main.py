from sheet_handles import NetWorthHandle

def main():
    net_worth = NetWorthHandle()
    sheet = net_worth.sheet.get_worksheet(0)
    print(sheet.get('C1'))

if __name__ == '__main__':
    main()