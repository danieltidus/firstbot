from exchange import Exchange;
from lib.poloniexWrapper import poloniex;

class Poloniex (Exchange):

    def __init__(self, apiKey, secret):
        super(Poloniex, self).__init__(Poloniex.__name__, apiKey);
        self.pol = poloniex(apiKey, secret);

    def getApiKey(self):
        return self.apiKey + " da Poloniex";

    def getBid(self, currencyPair):
        try:
            return float(self.pol.returnTicker()[currencyPair]["highestBid"]);
        except Exception, error:
            print("Error getting Bid");
            print str(error);
            return 0.0;

    def getAsk(self, currencyPair):
        try:
            return float(self.pol.returnTicker()[currencyPair]["lowestAsk"]);
        except Exception, error:
            print("Error getting Ask");
            print str(error);
            return 0.0;

    def ticker(self):
        try:
            return self.pol.returnTicker();
        except Exception, error:
            print("Error accessing ticker!");
            print str(error);
            return {};

    def tradableBalances(self):
        return self.pol.returnTradableBalances();

    #Return exchange fee. You must multiply by 100 to get fee in percentage
    def getFee(self):
        return float(self.pol.returnFeeInfo()["takerFee"]);

    def getOrderBook(self, currencyPair, type, depth=10):
        data = self.pol.returnOrderBook(currencyPair)
        asks = data['asks']
        bids = data['bids']
        firstPairs = {'asks': asks[:depth], 'bids': bids[:depth]}
        return firstPairs[type]

    def buy(self, currencyPair, price, amount):
        return self.pol.buy(currencyPair, price, amount)

    #Return balance by currnency. Return -1 if a invalid currency is passed
    def getBalance(self, currency):
        try:
            return  float(self.pol.returnBalances()[currency])
        except KeyError as e:
            print "KeyError: " + str(e)
            return -1

    def returnOpenOrders(self, currencyPair):
        return self.pol.returnOpenOrders(currencyPair)

    #Creating long and shorts sets of pairs.
    def getLongShortPairs(self):
        long_pairs = {}
        short_pairs = {}
        m_type = {}

        try:
            result = self.ticker()

            for key in result.keys():
                str_array = key.split('_')
                long_pairs[str_array[1]] = str_array[0]

            m_type["LONG"] = long_pairs

            result = self.tradableBalances()

            for key in result.keys():
                str_array = key.split('_')
                short_pairs[str_array[1]] = str_array[0]

            m_type["SHORT"] = short_pairs

        except Exception, error:
            print("Error on method getLongShortPairs!")
            print str(error)
            m_type["LONG"] = {}
            m_type["SHORT"] = {}

        finally:
            return m_type
