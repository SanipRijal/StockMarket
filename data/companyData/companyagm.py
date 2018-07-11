#!/usr/bin/python3.6
import urllib

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup as soup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from data.companyData.company import companyList

#get the list of all the listed companies
def getCompanyList():
    company_list = []
    class AppURLOpener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"

    opener = AppURLOpener()

    #display = Display(visible=0, size=(800, 600))
    #display.start()

    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")

    # #opening an instance of browser
    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=options)

    # goto browser
    driver.get("http://www.nepalstock.com.np/company")
    element = driver.find_element_by_name('_limit')
    element.send_keys(500)
    option = driver.find_element_by_xpath("//input[@value='Filter']")
    option.click()
    company_page = driver.page_source
    s = soup(company_page, 'html.parser')
    table = s.find('table', class_='my-table')
    data = table.find_all('tr')
    index = slice(2, len(data) - 1)
    data = data[index]

    cmpSymbol = []
    for row in data:
        cols = row.find_all('td')
        rindex = slice(0, len(cols) - 1)
        cols = cols[rindex]
        cols = [x.text.strip() for x in cols]
        serial_no = cols[0]
        name = cols[2]
        symbol = cols[3]
        category = cols[4]
        c = companyList(serial_no, name, symbol, category)
        company_list.append(c)
        cmpSymbol.append(symbol)

    return cmpSymbol

#get the company stock details
def getCompanyStock(symbol):
    companyData = []   #list to store the stock data of companies

    #to open the browser in background
    display = Display(size=(1000, 1000))
    display.start()

    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")

    #opening an instance of browser
    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=options)

    #website to fetch data from
    driver.get("http://merolagani.com/CompanyDetail.aspx?symbol=" + symbol)

    link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@title='Annual General Meeting']"))
    )

    link.click()

    html = driver.page_source
    page = soup(html, "html.parser")
    div = page.find("div", attrs={"id": "ctl00_ContentPlaceHolder1_CompanyDetail1_divAgmData"})
    table = div.find("table")
    tbody = table.find("tbody")
    tr = tbody.findAll("tr")
    index = slice(1, len(tr) - 1)
    tr = tr[index]

    data = []
    for row in tr:
        td = row.findAll("td")
        fiscal = td[1].text
        dividend = td[5].text
        bonus = td[6].text
        try:
            rightshare = td[7].text
        except:
            rightshare = 0

        d = [fiscal, dividend, bonus, rightshare]
        data.append(d)

    df = pd.DataFrame(data)
    file = symbol + '/agm.csv'
    with open(file, 'a') as f:
        df.to_csv(f, header=False, mode='a', index=False)

def main():
    symbol = getCompanyList()#gets the company symbol list
    print(symbol)
    for symb in symbol:   #loop for each symbol
        getCompanyStock(symb)  #get the company stock data

if __name__ == '__main__':
    main()