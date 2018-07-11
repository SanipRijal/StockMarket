#!/usr/bin/python3
# -*- coding: utf-8 -*-

import calendar
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup as soup


columns = ['Date', 'Value', 'Change', 'Percentage change']

# display = Display(visible=0, size=(600, 400))
# display.start()

options = webdriver.ChromeOptions()
options.add_argument("--incognito")

#opening an instance of browser
driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=options)
driver.get("http://merolagani.com/Indices.aspx")

index = Select(driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlIndexFilter"))
index.select_by_visible_text("NEPSE")

nepseData = []

driver.find_element_by_id("ctl00_ContentPlaceHolder1_lbtnSearchIndices").click()
loop = True

while loop:
    html = driver.page_source
    s = soup(html, "html.parser")
    table = s.find("table", attrs={"class":"table table-bordered table-striped table-hover sortable"})
    tbody = table.find("tbody")
    tr = tbody.findAll("tr")
    for row in tr:
        td = row.findAll("td")
        date = td[1].text
        value = float(td[2].text.replace(",", ""))
        change = float(td[3].text)
        percentage_change = float(td[4].text.replace("%",""))
        d = [date, value, change, percentage_change]
        print(d)
        nepseData.append(d.copy())
        driver.implicitly_wait(10)
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
# display.stop()

print(nepseData)
df = pd.DataFrame(nepseData)
#open 'data.csv' file for appending
with open('nepse.csv', 'a') as f:
    #add the dataframe to the file
    df.columns = columns
    df.to_csv(f, header = False, encoding = 'utf-8', index=False, mode='a')






