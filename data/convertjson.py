import csv
import json

data=[]
Company={}
companyData = []
prevSymbol=""

#open the csv file
file = open('companyData/AVU/pricehistory.csv', 'r')
reader = csv.reader(file, delimiter=',')
for item in reader:
    date_value=()
    new = 0
    symbol = item[0]

    if(symbol!=prevSymbol):
        new = 1

    date_value = date_value+(item[1], item[2])
    prevSymbol = item[0]

    if(new == 1):
        companyData.append(Company)
        Company={}
        data=[]

    data.append(date_value)
    Company[symbol] = data

companyData.append(Company)

with open('companyData/AVU/pricehistory.json', 'w') as f:
    json.dump(companyData, f)
