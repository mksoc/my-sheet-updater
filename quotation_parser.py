import config
import requests
from PyPDF2 import PdfReader
import dateparser

class QuotationParser():
    url = config.quotation_url
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

    def get_price(self, item):
        # Different behavior if the pattern to look for is 
        # a simple string or a sequence of strings to match
        pattern = item["pattern"]
        offset = item["offset"]

        if isinstance(pattern, list):
            for i in range(len(self.text) - len(pattern) + 1):
                if self.text[i:i+len(pattern)] == pattern:
                    price_index = (i + len(pattern) - 1) + offset
                    break
        else:
            price_index = self.text.index(pattern) + offset

        try:
            # Remove Italian thousands marker and change decimal separator
            price = float(self.text[price_index].replace('.','').replace(',', '.'))
        except (ValueError, TypeError):
            print(f'Could not find valid price of "{item}". Please check the PDF manually.')
            exit(1)

        return price

    def get_date(self):
        return dateparser.parse(' '.join(self.text[0:3]), languages=['it'], settings={'TIMEZONE': 'UTC'})
