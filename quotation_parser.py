import requests
from PyPDF2 import PdfReader
import dateparser

class QuotationParser():
    url = 'https://www.cambiovarallo.it/Tabellacambi_LISTINI.pdf'
    filename = 'listino.pdf'

    def __init__(self):
        self.save_pdf()
        self.text = self.get_text()
    
    def save_pdf(self):
        response = requests.get(self.url)
        with open(self.filename, 'wb') as pdf_file:
            pdf_file.write(response.content)

    def get_text(self):
        reader = PdfReader(self.filename)
        page = reader.pages[0]
        return page.extract_text().split()


def main():
    parser = QuotationParser()
    date = dateparser.parse(' '.join(parser.text[0:3]), languages=['it'], settings={'TIMEZONE': 'UTC'})
    print(date)

if __name__ == "__main__":
    main()