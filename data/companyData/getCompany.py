#!/usr/bin/python3

#this program fetches all the companies listed along with their symbol from nepalstock.com.np

import urllib.request
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver
from data.companyData.company import companyList

company_list = []

def getCompanyList():
    class AppURLOpener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"

    opener = AppURLOpener()

    display = Display(visible=0, size=(800, 600))
    display.start()

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")

    # #opening an instance of browser
    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=options)



    # goto browser
    driver.get("http://www.nepalstock.com.np/company")
    element = driver.find_element_by_name('_limit')
    element.send_keys(500)
    option = driver.find_element_by_xpath("//input[@value='Filter']")
    option.click()
    company_page = driver.page_source
    soup = BeautifulSoup(company_page, 'html.parser')
    table = soup.find('table', class_='my-table')
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