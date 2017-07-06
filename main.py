from exchanges.exchangefactory import ExchangeFactory

fac = ExchangeFactory

a = fac.create('poloniex');
print a.getApiKey();

a = fac.create('bittrex');
print a.getApiKey();
