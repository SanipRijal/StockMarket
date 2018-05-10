#!/usr/bin/python3
# -*- coding: utf-8 -*-

import calendar
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup as soup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

cal = calendar.Calendar()

#display = Display(visible=0, size=(600, 400))
#display.start()

#options=Options()
#options.add_argument("--no-sandbox")
driver = webdriver.Chrome("/usr/bin/chromedriver")
driver.get("http://sharesansar.com/datewise-indices")

for year in range(2015, 2018):
    for month in range(1, 12):
        monthdays = [d for d in cal.itermonthdays(year, month) if d!=0]
        for day in monthdays:
            dateField = driver.find_element_by_name("date")
            dateField.clear()
            dateString = str(year) + "-" + str(month) + "-" + str(day)
            print(dateString)
            dateField.send_keys(dateString)

            driver.implicitly_wait(5)
            driver.find_element_by_xpath("//button[@id = 'search']").click()

            html = driver.page_source

            s = soup(html, "html.parser")
            table = s.find("table", attrs={"class": "table table-bordered table-striped table-hover"})
            tbody = table.find("tbody")
            tr = tbody.find_all("tr")
            for row in tr:
                td = row.find_all("td")
                for data in td:
                    print(td)