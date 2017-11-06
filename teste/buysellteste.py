import sys
sys.path.append('.')
from exchanges.exchangefactory import ExchangeFactory
import botlib
import pprint
import time
import ConfigParser


COIN_PAIR = 'BTC_CLAM'
#ORDER_NUMBER =119863928138
ORDER_NUMBER ='345584f3-5ff0-43c2-a65c-acd3b3fcc10a'
fac = ExchangeFactory()

exchanges = {'Poloniex': fac.create('Poloniex'), 'Bittrex': fac.create('Bittrex')}

pp = pprint.PrettyPrinter(indent=4)


#pp.pprint(exchanges['Poloniex'].getBid(COIN_PAIR))
#pp.pprint(exchanges['Poloniex'].getAsk(COIN_PAIR))

#UUID = exchanges['Bittrex'].sell(COIN_PAIR, 0.00760704,2)
#pp.pprint(UUID)
# pp.pprint(exchanges['Poloniex'].haveOpenOrder(COIN_PAIR))

config = ConfigParser.RawConfigParser();
config.read('bot.cfg');
ex1=config.get('General', 'Exchange1')
ex2=config.get('General', 'Exchange2')
print "Key da " + ex1 + " " + config.get(ex1, 'apiKey')
print "Secret da " + ex1 + " " + config.get(ex1, 'secret')
print "Fees na " + ex1 + " Maker: " + config.get(ex1, 'fee_maker') + " Taker: " + config.get(ex1, 'fee_taker')
print "Key da " + ex2 + " " + config.get(ex2, 'apiKey')
print "Secret da " + ex2 + " " + config.get(ex2, 'secret')
print "Fees na " + ex2 + " Maker: " + config.get(ex2, 'fee_maker') + " Taker: " + config.get(ex2, 'fee_taker')

print "spreadEntry: " + config.get('General', 'spreadEntry')
print "spreadTarget: " + config.get('General', 'spreadTarget')
print "simulationTime: " +config.get('General', 'simulationTime')
print "BTC amount: " + config.get('General', 'btc_amount')
print "Order Book Factor: " + config.get('General', 'orderBookFactor')


#Verify arbitrages for long/shorts combinations
#Parameters - TODO Put on config file;
spreadEntry=float(config.get('General', 'spreadEntry'))
spreadTarget=float(config.get('General', 'spreadTarget'))
simulationTime =float(config.get('General', 'simulationTime'))
btc_amount = float(config.get('General', 'btc_amount'))
orderBookFactor = float(config.get('General', 'orderBookFactor'))
print spreadEntry
print spreadTarget
print simulationTime
print btc_amount
print orderBookFactor
#########################

#Just for tests
fees = float(config.get(ex1, 'fee_maker')) + float(config.get(ex1, 'fee_taker')) + float(config.get(ex2, 'fee_maker')) + float(config.get(ex2, 'fee_taker'))
print "Total de fees: " + str(fees)

# print "Get Balance long..."
# balanceLong = exchanges['Bittrex'].getBalance('BTC')
#
# print "Get Balance short..."
# balanceShort = exchanges['Poloniex'].getBalance('BTC')
#
# print "BID VALUE"
# bidPrice = exchanges['Poloniex'].getBid(COIN_PAIR)
# pp.pprint(bidPrice)
#
# #Acessando valor para comprar
# print "ASK VALUE"
# askPrice = exchanges['Bittrex'].getAsk(COIN_PAIR)
# pp.pprint(askPrice)
#
# #Simulando um delay
# print "Domindo um pouco para simular um delay..."
# time.sleep(1)
#
# #Tentando comprar
# print "Teste::comprando...."
# the_order = botlib.secureIn(exchanges['Bittrex'], exchanges['Poloniex'],balanceLong, balanceShort, COIN_PAIR, askPrice, bidPrice)
#
# orderExecuted = False
#
# #Verificando se a ordem foi cadastrada, caso contratio nao tem o que fazer.
# if the_order != -1:
#
#     print "Teste::Dormir um pouco para esperar as ordens serem executadas"
#     # Aguardando um pouco pra ver se a ordem de compra eh executada
#     time.sleep(3)
#     #Verificando se foi executada (Warning: Aqui pode rolar o slipage
#     while orderExecuted != True:
#         open_orders_long = exchanges['Bittrex'].returnOpenOrders(COIN_PAIR)
#         open_orders_short = exchanges['Poloniex'].returnOpenOrders(COIN_PAIR)
#         if len(open_orders_long) > 0 or len(open_orders_short) > 0 :
#             print "Teste::Ordens nao executadas, vou dormir mais um pouco!"
#             time.sleep(2)
#         else:
#             orderExecuted = True
#             print "Teste::Nao tem ordens, xablau!"
#     pass
#     print "Teste::Ordem executada!"
# else:
#     print "Teste::Ordem de compra nao foi criada"
