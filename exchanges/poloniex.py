from exchange import Exchange;

class Poloniex (Exchange):
    def getApiKey(self):
        return self.apiKey + " da Poloniex";
