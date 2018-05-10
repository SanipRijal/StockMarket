#!/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium import webdriver
from pyvirtualdisplay import Display

class AppURLOpener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"
opener=AppURLOpener()

display = Display(visible=0, size=(800, 600))
display.start()

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")

# #opening an instance of browser
driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver',chrome_options=options)

#goto browser
driver.get("http://www.nepalstock.com.np/company")
element=driver.find_element_by_name('_limit')
element.send_keys(500)
option=driver.find_element_by_xpath("//input[@value='Filter']")
option.click()
company_page=driver.page_source
company_list={}
soup=BeautifulSoup(company_page,'html.parser')
table =  soup.find('table',class_='my-table')
data=table.find_all('tr')
index=slice(2,len(data)-1)
data=data[index]

for row in data:
    cols=row.find_all('td')
    rindex=slice(0,len(cols)-1)
    cols=cols[rindex]
    cols=[x.text.strip() for x in cols]
    company_list["serial_no"]=cols[0]
    company_list["name"] = cols[2]
    company_list["symbol"] = cols[3]
    company_list["category"] = cols[4]
    print(company_list)