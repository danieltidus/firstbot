from exchanges.poloniex import Poloniex;
from exchanges.bittrex import Bittrex;
import ConfigParser

class ExchangeFactory(object):

  def create(self, exchange):
    config = ConfigParser.RawConfigParser();
    config.read('bot.cfg');
    if exchange == 'Poloniex':
        return Poloniex(config.get('Poloniex', 'apiKey'), config.get('Poloniex', 'secret'));
    elif exchange == 'Bittrex':
        return Bittrex(config.get('Bittrex', 'apiKey'), config.get('Bittrex', 'secret'));
