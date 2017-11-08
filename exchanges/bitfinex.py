import time
from exchange import Exchange
from lib.bitfinexwrapper import bitfinex

class Bitfinex (Exchange):

    def __init__(self, apiKey, secret):
        super(Bitfinex, self).__init__(Bitfinex.__name__, apiKey)
        self.bif = bitfinex(apiKey, secret)

    def ticker(self, currencyPair):
         str_pair = currencyPair.split('_')
         pair = str_pair[0]+str_pair[1]
         return self.bif.ticker(pair.lower())



    def getBid(self, currencyPair):
        try:
            str_pair = currencyPair.split('_')
            pair = str_pair[0]+str_pair[1]
            return float(self.bif.ticker(pair.lower())['bid'])
        except Exception, error:
            print("[" + str(self.getExchangeName()) + "] Error getting Bid")
            print str(error)
            return 0.0

    def getAsk(self, currencyPair):
        try:
            str_pair = currencyPair.split('_')
            pair = str_pair[0]+str_pair[1]
            return float(self.bif.ticker(pair.lower())['ask'])
        except Exception, error:
            print("[" + str(self.getExchangeName()) + "] Error getting Ask")
            print str(error)
            return 0.0
