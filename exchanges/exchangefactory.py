from exchanges.poloniex import Poloniex;
from exchanges.bittrex import Bittrex;
import ConfigParser

class ExchangeFactory(object):

  def create(self, exchange):
    if exchange == 'poloniex':
        config = ConfigParser.RawConfigParser();
        config.read('bot.cfg');
        return Poloniex(config.get('poloniex', 'apiKey'), config.get('poloniex', 'secret'));
    elif exchange == 'bittrex':
        return Bittrex('Teste');
