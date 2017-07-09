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

    def getAsk(self, currencyPair):
        print "Method getAsk not implemented to " + self.exchangeName;

    def ticker(self):
        print "Method ticker not implemented to " + self.exchangeName;

    def tradableBalances(self):
        print "Method tradableBalances not implemented to " + self.exchangeName;

    #Creating long and shorts sets of pairs.
    def getLongShortPairs(self):
        print "Method getLongShortPairs not implemented to " + self.exchangeName;

    def teste(self):
        print "Method getLongShortPairs not implemented to " + self.exchangeName;

    def getFee(self):
        print "Method getFee not implemented to " + self.exchangeName;
