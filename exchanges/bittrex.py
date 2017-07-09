from exchange import Exchange;
from lib.bittrexWrapper import bittrex;

class Bittrex (Exchange):

    def __init__(self, apiKey, secret):
        super(Bittrex, self).__init__(Bittrex.__name__, apiKey);
        self.bit = bittrex(apiKey, secret);

    def getApiKey(self):
        return self.apiKey + " da Bittrex";

    def getFee(self):
        return 0.0025;

    def getBid(self, currencyPair):
        str_pair = currencyPair.split('_');
        pair = str_pair[0]+"-"+str_pair[1];
        return self.bit.get_ticker(pair)["result"]["Bid"];

    def getAsk(self, currencyPair):
        str_pair = currencyPair.split('_');
        pair = str_pair[0]+"-"+str_pair[1];
        return self.bit.get_ticker(pair)["result"]["Ask"];

    #Creating long and shorts sets of pairs.
    def getLongShortPairs(self):
        long_pairs = {};
        short_pairs = {};
        m_type = {};

        result = self.bit.get_markets();

        pairs = result["result"];

        for value in pairs:
            long_pairs[value["MarketCurrency"]] = value["BaseCurrency"];

        m_type["LONG"] = long_pairs;
        m_type["SHORT"] = short_pairs;

        return m_type;
