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


    #INFO: Method problably not needed on this exchange
    def tradableBalances(self):
        print "Method tradableBalances not implemented to " + self.exchangeName;
        return {}

    #Creating long and shorts sets of pairs.
    def getLongShortPairs(self):
        try:
            print "Method getLongShortPairs not implemented to " + self.exchangeName;
            long_pairs = {}
            short_pairs = {}
            m_type = {}
            m_type["LONG"] = {}
            m_type["SHORT"] = {}

            syms = self.bif.symbols()

            for sym in syms:
                if sym[3:] == "btc":
                    long_pairs[sym[:3].upper()] = sym[3:].upper()
            #Correcting bug on pair
            long_pairs.pop('BCC')
            m_type["LONG"] = long_pairs
            for sym in syms:
                if sym[3:] == "btc":
                    short_pairs[sym[:3].upper()] = sym[3:].upper()

            #Correcting bug on pair
            short_pairs.pop('BCC')
            m_type["SHORT"] = short_pairs

            print m_type

        except Exception, error:
            print("[Bitfinex] Error on method getLongShortPairs!")
            print str(error)
            m_type["LONG"] = {}
            m_type["SHORT"] = {}
        finally:
            return m_type


    def getAlias(self, currency):
        if currency == u'DSH':
            return u'DASH'
        if currency == u'BCH':
            return u'BCC'
        if currency == u'QTM':
            return u'QTUM'

        return currency
