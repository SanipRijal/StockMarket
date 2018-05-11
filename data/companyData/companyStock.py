#!/usr/bin/python3

class companyStock:
    symbol = ""
    date = ""
    ltp = 0.0
    change = 0.0
    high = 0.0
    low = 0.0
    open = 0.0
    quantity = 0.0
    turnover = 0.0

    def __init__(self, symbol, date, ltp, high, low, open, quantity, turnover):
        self.symbol = symbol
        self.date = date
        self.ltp = ltp
        self.change = ltp - open
        self.high = high
        self.low = low
        self.open = open
        self.quantity = quantity
        self.turnover = turnover

    def getDate(self):
        return self.date

    def getLTP(self):
        return self.ltp

    def getHigh(self):
        return self.high

    def getLow(self):
        return self.low

    def getOpen(self):
        return self.open

    def getQuantity(self):
        return self.quantity

    def getTurnOver(self):
        return self.turnover
