from exchange import Exchange;

class Bittrex (Exchange):
    def getApiKey(self):
        return self.apiKey + " da Bittrex";
