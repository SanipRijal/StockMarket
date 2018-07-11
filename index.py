#!usr/bin/python3
#Author: SanipRijal

#This program fetches the stock data of todays market from the website 'nepalstock.com.np' and saves the data creating an xml file.
#'data.xml' stores the obtained data. Everyday this program runs, it fetches the data and updates the xml file.

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as soup
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from dataCollect import Data

#obtains the html file of todays market floorsheet
def getHTML():
	#run the browser in the background
	display = Display(visible=0, size=(800, 600))
	display.start()
	options = Options()
	options.add_argument("--no-sandbox")
	driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=options)
	driver.get("http://nepalstock.com.np/todaysprice")
	
	#set the limit to the maximum data to be displayed in one place(500)
	limit = Select(driver.find_element_by_name("_limit"))	#_limit is the name for the select option in the browser
	limit.select_by_visible_text("500") 	#set the option to 500
	driver.find_element_by_xpath("//input[@value = 'Filter']").click() #click on the Filter button
	
	#get the html document of the obtained web page
	html = driver.page_source
	driver.quit()
	return html	

#to provide indentation to the obtained xml tree
def indent(elem, level=0):	#elem is the root element
	i = "\n" + level*"  "	#declaring the indentation

	if len(elem):
		if not elem.text or not elem.text.strip():
			elem.text = i + "  "
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
		for subelem in elem:
			indent(subelem, level+1)
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
	else:
		if level and (not elem.tail or not elem.tail.strip()):
			elem.tail = i

#to create an xml tree and save it in an xml document named "dta.xml"
#The xml tree will have the structure as:
#<date value = "some-value">
#	<Data>
#		<SN>"text"</SN>
#		<Company>"text"</Company>
#		...
#	</Data>
#</date>

#from the obtained html document, retrieve the data and store it in the xml file
def getAndSetData(html):
	page_soup = soup(html, "html.parser")

	#obtain the date of the data
	dateLabel = page_soup.find(id = 'date')
	dateSnip = dateLabel.text.replace('As of ', '')	#remove unwanted character
	date = dateSnip[:10]

	tree = ET.parse('data.xml')	#open the xml file and parse it

	root = tree.getroot()		#get the root element of the xml file

	#create a new sub element for the xml tree with todays date
	Date = SubElement(root, 'Date')
	Date.attrib["value"] = date	#declaring an attribute for the element

	#obtain the respective data of each companyData from the table in the webpage
	table = page_soup.find_all('table')[0]	#find the first table from the webpage and create a list
	data = table.find_all('tr')	#find all the 'tr' elements from table
	index = slice(2, len(data)-4)	#define the slice index.The needed data starts from index 2 and ends in index 'len(data)-4'of table
	data = data[index]

	for row in data:
		cols = row.find_all('td')	#find the 'td' elements
		cols = [x.text.strip() for x in cols] #obtains the text from the element
		#store the obtained data in the object
		obj = Data(date, cols[0], cols[1], cols[2], cols[3], cols[4], cols[5], cols[6], cols[7], cols[8], cols[9])

		#create a xml file containing the data obtained
		createXML(obj, Date)

	#indent the obtained xml tree
	indent(Date)
	#update the xml tree in the xml file "data.xml"
	tree.write("data.xml", xml_declaration = True, encoding = 'utf-8')
        
#create and update the xml
def createXML(obj, elem):
	
	Data = SubElement(elem,'Data')	#sub element for the xml tree
			
	#declaring the sub elements of the xml tree
	SN = SubElement(Data, 'SN')
	SN.text = obj.getSN()
		
	Company = SubElement(Data, 'Company')
	Company.text = obj.getNameOfCompany()

	NumberOfTransactions = SubElement(Data, 'NumberOfTransactions')
	NumberOfTransactions.text = obj.getTransactionNumber()

	MaxPrice = SubElement(Data, 'MaxPrice')
	MaxPrice.text = obj.getMaxPrice()
	
	MinPrice = SubElement(Data, 'MinPrice')
	MinPrice.text = obj.getMinPrice()
	
	ClosingPrice = SubElement(Data, 'ClosingPrice')
	ClosingPrice.text = obj.getClosingPrice()

	TradedShare = SubElement(Data, 'TradedShare')
	TradedShare.text = obj.getTradedShare()

	Amount = SubElement(Data, 'Amount')
	Amount.text = obj.getAmount()

	PrevClosing = SubElement(Data, 'PrevClosing')
	PrevClosing.text = obj.getPrevClosing()
	
	AmountDiff = SubElement(Data, 'AmountDiff')
	AmountDiff.text = obj.getAmountDiff()
	
	#append the obtained sub elements to the xml tree

def main():
	html = getHTML()	#gets the html file from the respective webpage
	getAndSetData(html)	#creates an xml tree and saves it in "data.xml"

if __name__ == "__main__":
	main()

