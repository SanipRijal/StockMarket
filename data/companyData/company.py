#!/usr/bin/python3

class companyList:
    serial_no = 0
    name = ""
    symbol = ""
    category = ""

    def __init__(self, serial_no, name, symbol, category):
        self.serial_no = serial_no
        self.name = name
        self.symbol = symbol
        self.category = category

    def getSerialNo(self):
        return self.serial_no

    def getName(self):
        return self.name

    def getSymbol(self):
        return self.symbol

    def getCategory(self):
        return self.category

    def setSerialNo(self, serial_no):
        self.serial_no = serial_no

    def setName(self, name):
        self.name = name

    def setSymbol(self, symbol):
        self.symbol = symbol

    def setCategory(self, category):
        self.category = category
