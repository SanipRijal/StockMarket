import urllib

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from data.companyData.company import companyList

# This script fetches the company list and stores their information in a csv file

#set the display option of the Dataframe
pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1000)

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
    soup = BeautifulSoup(company_page, 'html.parser')
    table = soup.find('table', class_='my-table')
    data = table.find_all('tr')
    index = slice(2, len(data) - 1)
    data = data[index]

    companyData = []

    for row in data:
        cols = row.find_all('td')
        rindex = slice(0, len(cols) - 1)
        cols = cols[rindex]
        cols = [x.text.strip() for x in cols]
        name = cols[2]
        symbol = cols[3]
        category = cols[4]
        details = [symbol, name, category]
        companyData.append(details)

    df = pd.DataFrame(companyData, columns=['symbol', 'name', 'category'])
    with open('companies.csv', 'a') as f:
        df.columns = ['symbol', 'name', 'category']
        df.to_csv(f, header=False, mode='a', index=False)

if __name__ == '__main__':
    getCompanyList()
