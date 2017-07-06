class Exchange(object):
    def __init__(self, apiKey):
        self.apiKey = apiKey

    def getApiKey(self):
        return self.apiKey;

    def setApiKey(self, apiKey):
        self.apiKey = apiKey;
