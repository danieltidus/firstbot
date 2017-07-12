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

         try:
             str_pair = currencyPair.split('_');
             pair = str_pair[0]+"-"+str_pair[1];
             return self.bit.get_ticker(pair)["result"]["Bid"];
         except Exception, error:
             print("Error getting Bid");
             print str(error);
             return 0.0;


    def getAsk(self, currencyPair):
        try:
            str_pair = currencyPair.split('_');
            pair = str_pair[0]+"-"+str_pair[1];
            return self.bit.get_ticker(pair)["result"]["Ask"];
        except Exception, error:
            print("Error getting Ask");
            print str(error);
            return 0.0;


    #Creating long and shorts sets of pairs.
    def getLongShortPairs(self):
        long_pairs = {};
        short_pairs = {};
        m_type = {};

        try:
            result = self.bit.get_markets();

            pairs = result["result"];

            for value in pairs:
                long_pairs[value["MarketCurrency"]] = value["BaseCurrency"];

            #TODO Bug on bittrex for this pairs. FIXME add BTC-LTC, BTC-ETH and BTC-XRP hardcoded;
            long_pairs['LTC'] = 'BTC';
            long_pairs['ETH'] = 'BTC';
            long_pairs['XRP'] = 'BTC';

            m_type["LONG"] = long_pairs;
            m_type["SHORT"] = short_pairs;

        except Exception, error:
            print("Error getting Long short pairs for Bittrex");
            print str(error);
            m_type["LONG"] = {};
            m_type["SHORT"] = {};

        finally:
            return m_type;
