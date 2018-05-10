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

display = Display(visible=0, size=(600, 400))
display.start()

options=Options()
options.add_argument("--no-sandbox")
driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)
driver.get("http://merolagani.com/Indices.aspx")

index = Select(driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlIndexFilter"))
index.select_by_visible_text("NEPSE")

nepse ={}

fromDateField = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtFromDateFilter")
toDateField = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtToDateFilter")
fromDateField.clear()
toDateField.clear()
fromDateField.send_keys("02/02/2014")
toDateField.send_keys("05/10/2018")

driver.find_element_by_id("ctl00_ContentPlaceHolder1_lbtnSearchIndices").click()
while EC.presence_of_element_located((By.XPATH, "//a[@title = 'Next Page']")):
    html = driver.page_source
    s = soup(html, "html.parser")
    table = s.find("table", attrs={"class":"table table-bordered table-striped table-hover sortable"})
    tbody = table.find("tbody")
    tr = tbody.findAll("tr")
    for row in tr:
        td = row.findAll("td")
        nepse["date"] = td[1].text
        nepse["value"] = td[2].text
        nepse["change"] = td[3].text
        nepse["%change"] = td[4].text
        print(nepse)
    driver.find_element_by_link_text("Next").click()
    driver.implicitly_wait(3)
display.stop()




