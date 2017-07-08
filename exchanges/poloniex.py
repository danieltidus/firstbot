from exchange import Exchange;
from lib.poloniexWrapper import poloniex;

class Poloniex (Exchange):

    def __init__(self, apiKey, secret):
        self.apiKey = apiKey
        self.pol = poloniex(apiKey, secret);

    def getApiKey(self):
        return self.apiKey + " da Poloniex";

    def ticker(self):
        return self.pol.returnTicker();

    def tradableBalances(self):
        return self.pol.returnTradableBalances();

    #Creating long and shorts sets of pairs.
    def getLongShortPairs(self):
        long_pairs = {};
        short_pairs = {};
        m_type = {};

        result = self.ticker();

        for key in result.keys():
            print key;
            str_array = key.split('_');
            long_pairs[str_array[1]] = [str_array[0]];


        m_type["LONG"] = long_pairs;

        result = self.tradableBalances();

        for key in result.keys():
            str_array = key.split('_');
            short_pairs[str_array[1]] = [str_array[0]];

        m_type["SHORT"] = short_pairs;
        return m_type;
