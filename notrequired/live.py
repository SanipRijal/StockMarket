#Author: SanipRijal

#this program fetches the live data from the nepalstockmarket.com.np

from bs4 import BeautifulSoup as soup
import urllib.request
import urllib.parse as uparse
from pandas import DataFrame, read_csv
import pandas as pd
from datetime import datetime
import time

#define the columns for the pandas Dataframe
col = ['Date', 'Name', 'LTP', 'LTV', 'PointChange', 'Open', 'High', 'Low', 'Volume', 'PrevClosing']

#set the display option of the Dataframe
pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1000)

#get the html pageof the url
def getHtml():
    #fetch the html from the url provided
    class AppURLOpener(urllib.request.FancyURLopener):
           version = "Mozilla/5.0"
    opener = AppURLOpener()

    url = "http://nepalstock.com.np/stocklive"
    uClient = opener.open(url)
    html = uClient.read()
    uClient.close()
    return html

#fetches the live data from each row
def getTableData(trow):
    rows_list = []

    #loop for each found row
    for data in trow:
        att = data.find_all('td')[1]    #take the second data
        title = att.get('title')    #fetch the title of the element
        att = data.find_all('td')[2]    #the third data
        ltp = att.text.strip()  #ltp 
        att = data.find_all('td')[3]    #the fourth data
        ltv = att.text.strip()  #ltv
        att = data.find_all('td')[4]    #the fifth data
        pointChange = att.text.strip()  #change in point
        att = data.find_all('td')[6]
        opened = att.text.strip()
        att = data.find_all('td')[7]
        high = att.text.strip()
        att = data.find_all('td')[8]
        low = att.text.strip()
        att = data.find_all('td')[9]
        volume = att.text.strip()
        att = data.find_all('td')[10]
        prevClosing = att.text.strip()
        #set the date to current date and time
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #create a dataset for the dataframe
        dataSet = [date,title, ltp, ltv, pointChange, opened, high, low, volume, prevClosing]
        #update the list
        rows_list.append(dataSet)
    return rows_list

#get the data from the html page
def getData():
    html = getHtml()

    page_soup = soup(html, "html.parser")
    try:
        #find the element with id 'home-contents'
        home_contents = page_soup.find(id = 'home-contents')
    except AttributeError as e:
        print("No element with id 'home-contents' found, exiting")
        return 1

    try:
        #fetch the div with class name as mentioned 
        table = page_soup.find('div', attrs = {"class": "col-xs-12 col-md-9 col-sm-9"})
    except AttributeError as e:
        print("No div found with the provided attributes, exiting")
        return 1
    try:
        #get the table body
        tbody = table.find('tbody')

    except AttributeError as e:
        print('No table body found, exiting')
        return 1
    try:
        #find all the rows in the table body
        trow = tbody.findAll('tr')
    except AttributeError as e:
        print("No table row found, exiting")
        return 1

    #get the live data from the table
    live_data = getTableData(trow)
    return live_data

def main():
    #set now as the current datetime
    now = datetime.now()
    #set end as the time '15:00:00' i.e. 3:00 pm
    end = datetime.strptime('15:00:00', '%H:%M:%S')

    #loop until true
    while True:
        data = getData()
        #add the data to the dataframe
        df = pd.DataFrame(data)
        #open 'data.csv' file for appending
        with open('data.csv', 'a') as f:
            #add the dataframe to the file
            df.to_csv(f, header = False, sep = '\t', encoding = 'utf-8')
        #if current time exceeds end time then break the loop
        if now.time() > end.time():
            break
        #sleep for 30 seconds
        time.sleep(30)

if __name__ == "__main__":
    main()
