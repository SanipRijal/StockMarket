#!/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from data.companyData.companyStock import companyStock
from data.companyData.getCompany import getCompanyList

def getCompanyStock(symbol):
    companyData = []
    class AppURLOpener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"

    opener = AppURLOpener()

    # display = Display(visible=0, size=(800, 600))
    # display.start()

    # options = webdriver.ChromeOptions()
    # options.add_argument("--no-sandbox")

    # #opening an instance of browser
    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver')  # ,chrome_options=options)

    driver.get("http://merolagani.com/CompanyDetail.aspx?symbol=" + symbol)
    driver.find_element_by_link_text("Price History").click()
    while EC.presence_of_element_located((By.XPATH, "//a[@title = 'Next Page']")):
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        div = soup.find("div", attrs={"id":"ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"})
        table = div.find("table")
        tbody = table.find("tbody")
        tr = tbody.findAll("tr")
        index = slice(1, len(tr) - 1)
        tr = tr[index]

        for data in tr:
            td = data.findAll("td")
            Date = td[1].text
            LTP = float(td[2].text.replace(",", ""))
            High = float(td[4].text.replace(",", ""))
            Low = float(td[5].text.replace(",", ""))
            Open = float(td[6].text.replace(",", ""))
            Quantity = float(td[7].text.replace(",", ""))
            Turnover = float(td[8].text.replace(",", ""))
            c = companyStock(symbol, Date, LTP, High, Low, Open, Quantity, Turnover)
            companyData.append(c)

        driver.find_element_by_link_text("Next").click()
        driver.implicitly_wait(3)

    return companyData

def main():
    symbol = getCompanyList()
    for symb in symbol:
        data = getCompanyStock(symb)
    for i in range(0, len(data)-1):
        print(data[i].getOpen())

if __name__ == '__main__':
    main()