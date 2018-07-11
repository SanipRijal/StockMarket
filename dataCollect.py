#!usr/bin/python3
#Author: SanipRijal

class Data:
	
	title = ['S.N.', 'Traded Companies', 'No. Of Transaction', 'Max Price', 'Min Price', 'Closing Price', 'Traded Shares', 'Amount', 'Previous Closing','Difference']
	#parameterized constructor for the class
	def __init__(self, date, SN, nameOfCompany, transactionNumber, maxPrice, minPrice, closingPrice, tradedShare, amount, prevClosing, amountDiff):
		self.date = date
		self.SN = SN
		self.nameOfCompany = nameOfCompany
		self.transactionNumber = transactionNumber
		self.maxPrice = maxPrice
		self.minPrice = minPrice
		self.closingPrice = closingPrice
		self.tradedShare = tradedShare
		self.amount = amount
		self.prevClosing = prevClosing
		self.amountDiff = amountDiff
	
	#getters and setters for the class members

	def getTitle(self, index):
		return self.title[index]
	
	def setDate(self, date):
		self.date = date

	def setSN(self, SN):
		self.SN = SN
	
	def setNameOfCompany(self, nameOfCompany):
		self.nameOfCompany = nameOfCompany
	
	def setTransactionNumber(self, transactionNumber):
		self.transactionNumber = transactionNumber
		
	def setMaxPrice(self, maxPrice):	
		self.maxPrice = maxPrice
	
	def setMinPrice(self, minPrice):
		self.minPrice = minPrice
	
	def setClosingPrice(self, closingPrice):
		self.closingPrice = closingPrice
	
	def setTradedShare(self, tradedShare):
		self.tradedShare = tradedShare

	def setAmount(self, amount):
		self.amount = amount
	
	def setPrevClosing(self, prevClosing):
		self.prevClosing = prevClosing
	
	def setAmountDiff(self, amountDiff):
		self.amountDiff = amountDiff
	
	def getDate(self):
		return self.date
	
	def getSN(self):
		return self.SN
	
	def getNameOfCompany(self):
		return self.nameOfCompany
	
	def getTransactionNumber(self):
		return self.transactionNumber
	
	def getMaxPrice(self):	
		return self.maxPrice
	
	def getMinPrice(self):
		return self.minPrice
	
	def getClosingPrice(self):
		return self.closingPrice
	
	def getTradedShare(self):
		return self.tradedShare
	
	def getAmount(self):
		return self.amount
	
	def getPrevClosing(self):
		return self.prevClosing

	def getAmountDiff(self):
		return self.amountDiff
