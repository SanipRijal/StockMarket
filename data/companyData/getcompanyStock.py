import urllib

from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from data.companyData.company import companyList
from data.companyData.companyStock import companyStock

#This script fetches the stock data of all listed companies

#set the display option of the Dataframe
pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1000)

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

#get the company stock details
def getCompanyStock(symbol):
    companyData = []   #list to store the stock data of companies

    #to open the browser in background
    #display = Display(visible=0, size=(1000, 1000))
    #display.start()

    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")

    #opening an instance of browser
    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=options)

    #website to fetch data from
    driver.get("http://merolagani.com/CompanyDetail.aspx?symbol=" + symbol)
    #driver waits until the element 'a' with title Price History is not located in the page
    link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@title='Price History']"))
    )

    #click the link
    link.click()
    loop = True

    #loop until the element with title 'next page' is found in page
    while loop:
        # disable the date field
        textbox = driver.find_element_by_id("ctl00_ContentPlaceHolder1_CompanyDetail1_txtMarketDatePriceFilter")
        driver.execute_script("arguments[0].disabled = true", textbox)
        # get the page html
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # get the data from the table
        div = soup.find("div", attrs={"id": "ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"})
        table = div.find("table")
        tbody = table.find("tbody")
        tr = tbody.findAll("tr")

        # manage the index required
        index = slice(1, len(tr) - 1)
        tr = tr[index]
        # loop for each data in the row
        for data in tr:
            td = data.findAll("td")
            Date = td[1].text
            LTP = float(td[2].text.replace(",", ""))
            High = float(td[4].text.replace(",", ""))
            Low = float(td[5].text.replace(",", ""))
            Open = float(td[6].text.replace(",", ""))
            Quantity = float(td[7].text.replace(",", ""))
            Turnover = float(td[8].text.replace(",", ""))

            # pass the values to the constructor companyStock
            c = companyStock(symbol, Date, LTP, High, Low, Open, Quantity, Turnover)
            # add the data to the list
            d = [symbol, Date, LTP, High, Low, Open, Quantity, Turnover]
            companyData.append(d)
            print(Date, LTP, Low, Open, Quantity, Turnover)


        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@title='Market']"))
        )
        driver.implicitly_wait(5)
        dropdown.click() #to avoid the date  picker from popping up
        try:
            driver.find_element_by_link_text("Last")
        except NoSuchElementException:
            loop = False
        if loop == False:
            break
        else:
            try:
                driver.implicitly_wait(5)
                driver.find_element_by_link_text("Next").click()
            except NoSuchElementException:
                print("Next not clickable")

    df = pd.DataFrame(companyData, columns=['Symbol','Date', 'LTP', 'High', 'Low', 'Open', 'Quantity', 'Turnover'])
    file = symbol + '/pricehistory.csv'
    with open(file, 'a') as f:
        df.columns= ['Symbol','Date', 'LTP', 'High', 'Low', 'Open', 'Quantity', 'Turnover']
        df.to_csv(f, header=False, mode='a', index=False)
    driver.quit()
    return companyData#return the company data

def main():
    symbol = getCompanyList()#gets the company symbol list
    for symb in symbol:   #loop for each symbol
        getCompanyStock(symb)  #get the company stock data

if __name__ == '__main__':
    main()
