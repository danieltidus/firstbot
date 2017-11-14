import sys
sys.path.append('.')
from exchanges.exchangefactory import ExchangeFactory
import botlib
import pprint
import time
import ConfigParser
import utils


COIN_PAIR = 'BTC_XMR'
#ORDER_NUMBER =119863928138
ORDER_NUMBER ='345584f3-5ff0-43c2-a65c-acd3b3fcc10a'
fac = ExchangeFactory()

exchanges = {'Bittrex': fac.create('Bittrex'), 'Poloniex': fac.create('Poloniex')}

pp = pprint.PrettyPrinter(indent=4)

print "Pares Poloniex"
pp.pprint(exchanges['Poloniex'].getLongShortPairs())

print "Combinations"
pp.pprint(botlib.findCombinations(exchanges))

#pp.pprint(exchanges['Poloniex'].getBid(COIN_PAIR))
#pp.pprint(exchanges['Poloniex'].getAsk(COIN_PAIR))

#UUID = exchanges['Poloniex'].sell(COIN_PAIR, 0.00760704,2)
#pp.pprint(UUID)
# pp.pprint(exchanges['Poloniex'].haveOpenOrder(COIN_PAIR))

#print  exchanges['Poloniex'].getOrderBTCValue('ef565f3a-788a-4fc8-8c33-1c86c74209df')

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
