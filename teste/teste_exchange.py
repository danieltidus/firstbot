import sys
sys.path.append('.')
import pprint
from exchanges.exchangefactory import ExchangeFactory
from datetime import datetime



fac = ExchangeFactory()
exchange = fac.create('Bitfinex')

currencyPair = 'BTC_USD'
apiKey='test'
price=0.0001
amount=0.01
orderNumber='das4d5as'
currency='BTC'

pp = pprint.PrettyPrinter(indent=4)

print "\n[ " + str(datetime.now().ctime()) + " ] " + "Calling getExchangeName()"
exchange.getExchangeName()

print "\n[ " + str(datetime.now().ctime()) + " ] " + "Calling getApiKey()"
print exchange.getApiKey()

print "\n[ " + str(datetime.now().ctime()) + " ] " + "Calling setApiKey()"
exchange.setApiKey(apiKey)

print "\n[ " + str(datetime.now().ctime()) + " ] " + "Calling ticker()"
pp.pprint(exchange.ticker(currencyPair))

print "\n[ " + str(datetime.now().ctime()) + " ] " + "Calling getBid()"
print exchange.getBid(currencyPair)

print "\n[ " + str(datetime.now().ctime()) + " ] " + "Calling getAsk()"
print exchange.getAsk(currencyPair)

print "\n[ " + str(datetime.now().ctime()) + " ] " + "Calling tradableBalances()"
exchange.tradableBalances()

print "\n[ " + str(datetime.now().ctime()) + " ] " + "Calling getLongShortPairs()"
exchange.getLongShortPairs()

print "\n[ " + str(datetime.now().ctime()) + " ] " + "Calling getFee()"
exchange.getFee()

print "\n[ " + str(datetime.now().ctime()) + " ] " + "Calling getOrderBook()"
exchange.getOrderBook(currencyPair, 'asks')

print "\n[ " + str(datetime.now().ctime()) + " ] " + "Calling buy()"
exchange.buy(currencyPair, price, amount)

print "\n[ " + str(datetime.now().ctime()) + " ] " + "Calling sell()"
exchange.sell(currencyPair, price, amount)

print "\n[ " + str(datetime.now().ctime()) + " ] " + "Calling buyMargin()"
exchange.buyMargin(currencyPair, price, amount)

print "\n[ " + str(datetime.now().ctime()) + " ] " + "Calling sellMargin()"
exchange.sellMargin(currencyPair, price, amount)

print "\n[ " + str(datetime.now().ctime()) + " ] " + "Calling getBalance()"
exchange.getBalance(currency)

print "\n[ " + str(datetime.now().ctime()) + " ] " + "Calling getMarginBalance()"
exchange.getMarginBalance(currencyPair)

print "\n[ " + str(datetime.now().ctime()) + " ] " + "Calling hasOpenOrder()"
exchange.hasOpenOrder(currencyPair)

print "\n[ " + str(datetime.now().ctime()) + " ] " + "Calling returnOpenOrders()"
exchange.returnOpenOrders(currencyPair)

print "\n[ " + str(datetime.now().ctime()) + " ] " + "Calling getOrderBTCValue()"
exchange.getOrderBTCValue(orderNumber)

print "\n[ " + str(datetime.now().ctime()) + " ] " + "Calling closeMarginPosition()"
exchange.closeMarginPosition(currencyPair)

print "\n[ " + str(datetime.now().ctime()) + " ] " + "Calling closeAllPositions()"
exchange.closeAllPositions(currencyPair)
