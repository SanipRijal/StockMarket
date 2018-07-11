import psycopg2
import csv


conn = psycopg2.connect(dbname='stockmarket', user='postgres', password='postgres', host='localhost')
cur = conn.cursor()

file = open('sample.csv', 'r')
reader = csv.reader(file, delimiter=',')
for item in reader:
    symbol = item[0]
    print(symbol)
    date = item[1].replace("/","-")
    print(date)
    ltp = item[2]
    high = item[3]
    low = item[4]
    open = item[5]
    quant = item[6]
    turn = item[7]
    chg = float(item[2]) - float(item[5])
    chg=repr(chg)
    data = (date, ltp, chg, high, low, open, quant, turn, symbol)
    cur.execute("INSERT into analysis_companydata(date, ltp, change, high, low, open, quantity, turnover, symbol_id) \
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s)", data)
    conn.commit()
    print("Company Data added")


