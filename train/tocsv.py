#!bin/usr/python3

import xml.etree.ElementTree as ET
from pandas import DataFrame, read_csv
import pandas as pd

tree = ET.parse('/home/sanip/python/stockMarket/data.xml')
root = tree.getroot()

col = ['Date', 'Price']
pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 2)
pd.set_option('display.width', 100)

dataset = []
price = 0.0

for date in root.findall('Date'):
    dt = (date.get('value'))
    for data in date.findall('Data'):
        if data.find('Company').text == 'Arun Kabeli Power Ltd.':
            price = data.find('ClosingPrice').text
    d = [dt, price]
    dataset.append(d)

df = pd.DataFrame(dataset)
with open('sample.csv', 'w') as f:
    df.to_csv(f, header = False, sep = '\t', encoding = 'utf-8')




