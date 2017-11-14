import time
from exchange import Exchange
from lib.bittrexWrapper import bittrex

class Bittrex (Exchange):

    def __init__(self, apiKey, secret):
        super(Bittrex, self).__init__(Bittrex.__name__, apiKey)
        self.bit = bittrex(apiKey, secret)

    def getApiKey(self):
        return self.apiKey + " da Bittrex"

    def getFee(self):
        return 0.0025

    def getBid(self, currencyPair):

         try:
             str_pair = currencyPair.split('_')
             pair = str_pair[0]+"-"+str_pair[1]
             return self.bit.get_ticker(pair)["result"]["Bid"]
         except Exception, error:
             print("[Bittrex] Error getting Bid. Pair: " + str(currencyPair))
             print str(error)
             return 0.0


    def getAsk(self, currencyPair):
        try:
            str_pair = currencyPair.split('_')
            pair = str_pair[0]+"-"+str_pair[1]
            return self.bit.get_ticker(pair)["result"]["Ask"]
        except Exception, error:
            print("[Bittrex] Error getting Ask. Pair: " + str(currencyPair))
            print str(error)
            return 0.0

    def buy(self, currencyPair, price, amount):
        str_pair = currencyPair.split('_')
        pair = str_pair[0] + "-" + str_pair[1]
        try:
            response = self.bit.buy_limit(pair, amount, price)
            print response
            if response['success'] == True:
                return response['result']['uuid']
            else:
                return -1
        except Exception, error:
            print("[Bittrex] Error margin buying")
            print str(error)
            return -1

    def sell(self, currencyPair, price, amount ):
        str_pair = currencyPair.split('_')
        pair = str_pair[0] + "-" + str_pair[1]
        try:
            response = self.bit.sell_limit(pair, amount, price)
            print response
            if response['success'] == True:
                return response['result']['uuid']
            else:
                return -1
        except Exception, error:
            print("[Bittrex] Error margin buying")
            print str(error)
            return -1

    def getBalance(self, currency):
        try:
            msg = self.bit.get_balance(currency)
            if msg['success'] == True:
                l = msg['result']
                if l['Currency'] == currency:
                    if l['Balance'] != None:
                        return float(l['Balance'])
                    else:
                        return 0.0
            return -1
        except Exception, error:
            print("[Bittrex] Error getting balance!")
            print str(error)
            return -1

    def hasOpenOrder(self, currencyPair):
        # str_pair = currencyPair.split('_')
        # pair = str_pair[0] + "-" + str_pair[1]
        try:
            res = self.returnOpenOrders(currencyPair)
            print "Bittrex::haveOpenOrder()"
            if len(res) == 0:
                return False
            else:
                return True
        except Exception, error:
            print("[Bittrex] Error on haveOpenOrder()")
            print str(error)
            return False
    def returnOpenOrders(self, currencyPair):
        try:
            str_pair = currencyPair.split('_')
            pair = str_pair[0] + "-" + str_pair[1]
            response = self.bit.get_open_orders(pair)
            if response['success'] == True:
                return response['result']
            else:
                print("[Bittrex] Error on haveOpenOrder(). Requisition fail")
                return {}
        except Exception, error:
            print("[Bittrex] Error on haveOpenOrder()")
            print str(error)
            return {}

    def getOrderBTCValue(self, orderNumber):
        try:
            order = self.bit.get_order(orderNumber)
            print order
            if order['result']['QuantityRemaining'] == 0.0:
                value =  float(order['result']['Price'])
                value = value - value*0.0025
                return value
            else:
                print("[Bittrex] Error getting btc value of an order! Order still processing")
                return -1
        except Exception, error:
            print("[Bittrex] Error getting btc value of an order!")
            print str(error)
            return -1

    def getRealCost(self, amount):
         return (amount + amount*0.0025)

    def getOrderBook(self, currencyPair, type, depth=10):
        try:
            str_pair = currencyPair.split('_')
            pair = str_pair[0] + "-" + str_pair[1]
            response = self.bit.get_orderbook(pair, 'both', depth)
            if response['success'] == True:
                if type == 'asks':
                    list = response['result']['sell'][:depth]
                else:
                    list = response['result']['buy'][:depth]

                new_list = []
                for l in list:
                    new_list.append([l['Rate'], l['Quantity']])

                return new_list
            else:
                print("[Bittrex] Error on getOrderBook(). Requisition fail")
                return -1
            pass
        except Exception, error:
            print("[Bittrex] Error getting order book!")
            print str(error)
            return -1


    def closeAllPositions(self, currencyPair):
        #Cancelar ordem se for uma ordem em aberto
        str_pair = currencyPair.split('_')
        pair = str_pair[0] + "-" + str_pair[1]
        try:
            print "Tentando procurar a ordem no livro de ordens abertas..."
            res = self.bit.get_open_orders(pair)['result']
            for r in res:
                print "Achei ordem aberta, vou cancelar..."
                res = self.bit.cancel(r['OrderUuid'])
                if res['success'] ==  True:
                    print "Ordem " + str(r['OrderUuid']) + " cancelada com sucesso!"
                else:
                    print "Erro no cancelamento da ordem" + str(r['OrderUuid'])
                    return -1

            print "Transformar tudo que tiver dessa alt em btc"
            amount = self.getBalance(str_pair[1])

            if amount != 0:
                if amount != -1:
                    orderBookLong = self.getOrderBook(currencyPair, 'bids', 20)

                    altcoin_volume_avaiable_long = 0
                    newLongPrice = 0.0
                    # Calculating liquidity in each book
                    for x in orderBookLong:
                        altcoin_volume_avaiable_long += float(x[1])
                        newLongPrice = float(x[0])
                        if altcoin_volume_avaiable_long >= amount * 5:
                            break
                        pass
                    pass

                    if newLongPrice == 0.0:
                        print "Problemas no livro de ordens..."
                        return -1

                    order = self.sell(currencyPair, newLongPrice, amount)

                    if order != -1:
                        res = self.bit.get_order(order)
                        while res['result']['IsOpen'] == True:
                            print "Ordem esta cadastrada mas nao concluida, vamos esperar...Slippage??????"
                            time.sleep(3)
                        pass
                        print "Reversao concluida com sucesso"
                        return 0
                    else:
                        print "Problemas fechando a posicao. Ferrou!!!!!"
                        return -1
                else:
                    print "Erro acessando balanco"
                    return -1
            else:
                print "Sem balanco, vou encerrar!"
                return 0
            pass
        except Exception, error:
            print("[Bittrex] Error closing position!")
            print str(error)
            return -1



        #Se ja tiver sido executada, executar o reverso
        pass




    #Creating long and shorts sets of pairs.
    def getLongShortPairs(self):
        long_pairs = {}
        short_pairs = {}
        m_type = {}

        try:

            result = self.bit.get_markets()

            pairs = result["result"]
            for value in pairs:
                if value["BaseCurrency"] == "BTC":
                    long_pairs[value["MarketCurrency"]] = value["BaseCurrency"]
                    # long_pairs[value["MarketCurrency"]] = value["BaseCurrency"]

            #TODO Bug on bittrex for this pairs. FIXME add BTC-LTC, BTC-ETH and BTC-XRP hardcoded;
            long_pairs['LTC'] = 'BTC'
            long_pairs['ETH'] = 'BTC'
            long_pairs['XRP'] = 'BTC'
            long_pairs['XMR'] = 'BTC'
            long_pairs['DASH'] = 'BTC'
            long_pairs['FCT'] = 'BTC'
            # long_pairs['ZEC'] = 'BTC'

            m_type["LONG"] = long_pairs
            m_type["SHORT"] = short_pairs

        except Exception, error:
            print("Error getting Long short pairs for Bittrex")
            print str(error)
            m_type["LONG"] = {}
            m_type["SHORT"] = {}

        finally:
            return m_type
