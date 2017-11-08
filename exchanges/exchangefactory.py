from exchanges.poloniex import Poloniex;
from exchanges.bittrex import Bittrex;
from exchanges.bitfinex import Bitfinex;

import ConfigParser

class ExchangeFactory(object):

  def create(self, exchange):
    config = ConfigParser.RawConfigParser();
    config.read('bot.cfg');
    if exchange == 'Poloniex':
        return Poloniex(config.get('Poloniex', 'apiKey'), config.get('Poloniex', 'secret'));
    elif exchange == 'Bittrex':
        return Bittrex(config.get('Bittrex', 'apiKey'), config.get('Bittrex', 'secret'));
    elif exchange == 'Bitfinex':
        return Bitfinex(config.get('Bitfinex', 'apiKey'), config.get('Bitfinex', 'secret'));
