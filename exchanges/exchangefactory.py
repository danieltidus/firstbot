from exchanges.poloniex import Poloniex;
from exchanges.bittrex import Bittrex;

class ExchangeFactory(object):

  def create(self, exchange):
    if exchange == 'poloniex':
        return Poloniex('Teste');
    elif exchange == 'bittrex':
        return Bittrex('Teste');
