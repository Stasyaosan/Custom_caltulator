import requests
from lxml import etree
from datetime import datetime
import os


class ValCurs:
    def __init__(self):
        self.url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={datetime.now().strftime("%d/%m/%Y")}'
        self.load_file_xml()

    def load_file_xml(self):
        d = requests.get(self.url)
        if not os.path.exists('xml-data'):
            os.mkdir('xml-data')

        with open(f'xml-data/{datetime.now().strftime("%d-%m-%Y")}.xml', 'w') as f:
            f.write(d.text)

    def parse_with_xml(self):
        tree = etree.parse(f'xml-data/{datetime.now().strftime("%d-%m-%Y")}.xml')
        root = tree.getroot()
        date = root.get('Date')
        valute_dict = {}
        for valute in root.findall('Valute'):
            name = valute.find('Name').text
            value = valute.find('Value').text
            valute_dict[name] = value
        return valute_dict
