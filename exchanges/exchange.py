class Exchange(object):
    def __init__(self, exchangeName, apiKey):
        self.apiKey = apiKey
        self.exchangeName = exchangeName;

    def getExchangeName(self):
        return self.exchangeName;

    def getApiKey(self):
        return self.apiKey;

    def setApiKey(self, apiKey):
        self.apiKey = apiKey;

    def getBid(self, currencyPair):
        print "Method getBid not implemented to " + self.exchangeName;
        return 0.0

    def getAsk(self, currencyPair):
        print "Method getAsk not implemented to " + self.exchangeName;
        return 0.0

    def ticker(self):
        print "Method ticker not implemented to " + self.exchangeName;
        return {}

    def tradableBalances(self):
        print "Method tradableBalances not implemented to " + self.exchangeName;
        return {}

    #Creating long and shorts sets of pairs.
    def getLongShortPairs(self):
        print "Method getLongShortPairs not implemented to " + self.exchangeName;
        m_type = {}
        m_type["LONG"] = {}
        m_type["SHORT"] = {}
        return m_type

    def getFee(self):
        print "Method getFee not implemented to " + self.exchangeName;
        return 200

    def getOrderBook(self, currencyPair, type, depth=10):
        print "Method getOrderBook not implemented to " + self.exchangeName;
        return {}

    def buy(self, currencyPair, price, amount):
        print "Method buy not implemented to " + self.exchangeName;
        return -1

    def sell(self, currencyPair, price, amount):
        print "Method sell not implemented to " + self.exchangeName;
        return -1

    def buyMargin(self, currencyPair, price, amount):
        print "Method buyMargin not implemented to " + self.exchangeName;
        return -1

    def sellMargin(self, currencyPair, price, amount):
        print "Method sellMargin not implemented to " + self.exchangeName;
        return -1

    def getBalance(self, currency):
        print "Method getBalance not implemented to " + self.exchangeName;
        return -1

    def getMarginBalance(self, currencyPair):
        print "Method getMarginBalance not implemented to " + self.exchangeName;
        return -1

    def hasOpenOrder(self, currencyPair):
        print "Method hasOpenOrder not implemented to " + self.exchangeName;
        return False

    def returnOpenOrders(self, currencyPair):
        print "Method returnOpenOrders not implemented to " + self.exchangeName;
        return {}

    def getOrderBTCValue(self, orderNumber):
        print "Method getOrderBTCValue not implemented to " + self.exchangeName;
        return -1

    def closeMarginPosition(self, currencyPair):
        print "Method closeMarginPosition not implemented to " + self.exchangeName;
        return -1

    def closeAllPositions(self, currencyPair):
        print "Method closeAllPositions not implemented to " + self.exchangeName;
        return -1


    def getBTCByPair(self, currencyPair):
        print "Method getBTCByPair not implemented to " + self.exchangeName;
        return -1


    def returnHistory(self,currencyPair, days=3):
        print "Method returnHistory not implemented to " + self.exchangeName;
        return {}


    def getRealCost(self, amount):
        print "Method getRealCost not implemented to " + self.exchangeName;
        return -1
        
    def getAlias(self, currency):
        return currency
