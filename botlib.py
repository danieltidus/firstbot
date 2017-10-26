import pprint
import threading

# Receive a dict vector of exchanges and return a array of combinations
def findCombinations(exchanges={}):
    # Find possible combinations of short and long on exchanges
    pairsByExchange = {};
    combinations = [];

    for ex in exchanges:
        print "Get LongShortPairs to exchange: " + exchanges[ex].getExchangeName();
        pairsByExchange[exchanges[ex].getExchangeName()] = exchanges[ex].getLongShortPairs();

        # print "Long short to " + exchanges[ex].getExchangeName()
        # print pairsByExchange[exchanges[ex].getExchangeName()]
        # print "\n\n\n\n"
        pass
    id_ = 0;
    for ex in pairsByExchange:
        for pair_on_long in pairsByExchange[ex]["LONG"]:
            for other_ex in pairsByExchange:
                if other_ex != ex:
                    for pair_on_short in pairsByExchange[other_ex]["SHORT"]:

                        if (pair_on_short == pair_on_long):
                            if pairsByExchange[other_ex]["SHORT"][pair_on_short] == pairsByExchange[ex]["LONG"][
                                pair_on_long]:
                                str_pair = pairsByExchange[other_ex]["SHORT"][pair_on_short] + "_" + pair_on_short;
                                combinations.append({'id': id_, 'pair': str_pair, 'LongEx': ex, 'ShortEx': other_ex});
                                id_ = id_ + 1
                            pass

                        pass
                    pass
                pass
            pass
        pass
    pass

    return combinations









# Securely buy/sell an amount of coins based on lowest ask price of order book and an secure factor based on amount of coin available
#Return order to be checked or -1 if some error
def secureIn(exchangeLong, exchangeShort, balanceLong, balanceShort, currencyPair, askPrice, bidPrice, btc_amount=0.02, secureFactor=2, spreadTarget=-0.0008):
    pp = pprint.PrettyPrinter(indent=4)

    if askPrice <= 0 or bidPrice <=0:
        return -1000


    print "secureBuy::Balance on long exchange " + str(balanceLong)
    print "secureBuy::Balance on short exchange " + str(balanceShort)
    #No need balance available
    if balanceLong <= btc_amount or balanceShort <= btc_amount:
        print "secureBuy::No balance available. Verify long and short exchanges balance."
        return -1000

    print "secureBuy::Orderbook"
    orderBookLong = exchangeLong.getOrderBook(currencyPair, 'asks', 10)
    orderBookShort = exchangeShort.getOrderBook(currencyPair, 'bids', 10)

    print "Orderbook Long..."
    pp.pprint(orderBookLong)
    print "Orderbook Short..."
    pp.pprint(orderBookShort)

    print "secureBuy::Ask Price: " + "{:.8f}".format(askPrice) + ". Secure factor: " + str(secureFactor) + "x"
    print "secureBuy::Bid Price: " + "{:.8f}".format(bidPrice) + ". Secure factor: " + str(secureFactor) + "x"

    btc_volume_avaiable_long = 0  # Store the amount of available coins to buy converted in bitcoin
    btc_volume_avaiable_short = 0  # Store the amount of available coins to sell converted in bitcoin
    newAskPrice = 0.0
    newBidPrice = 0.0

    #Calculating liquidity in each book
    for x in orderBookLong:
        btc_volume_avaiable_long += float(x[0]) * float(x[1])
        newAskPrice = float(x[0])
        if btc_volume_avaiable_long >= btc_amount*secureFactor:
            break
        pass
    pass

    btc_volume_avaiable = 0
    for x in orderBookShort:
        btc_volume_avaiable_short += float(x[0]) * float(x[1])
        newBidPrice = float(x[0])
        if btc_volume_avaiable_short >= btc_amount*secureFactor:
            break
        pass
    pass

    print "secureBuy:: New Ask price " + str(newAskPrice)
    print "secureBuy:: New Bid price " + str(newBidPrice)

    #Verify if we have error with new prices
    if newAskPrice == 0.0 or newBidPrice == 0.0:
        print "secureBuy::Something wrong with order books. Stopping operations..."
        return -1000
    pass

    print "secureBuy:: BTC Amount available on Long " + str(btc_volume_avaiable_long)
    print "secureBuy:: BTC Amount available on short " + str(btc_volume_avaiable_short)
    # Verify if we have errors with liquidity
    if btc_volume_avaiable_long < btc_amount*secureFactor or btc_volume_avaiable_short < btc_amount*secureFactor:
        print "secureBuy::Not enough liquidity. Stopping operations..."
        return -1000
    pass

    print "secureBuy:: Current Spread " + str(spreadTarget)
    print "secureBuy:: New Spread " +  "{:.8f}".format(((newBidPrice - newAskPrice)/newAskPrice))

    # Verify if we have error with spreadTarget
    if spreadTarget > ((newBidPrice - newAskPrice)/newAskPrice):
        print "secureBuy::Invalid new spread. We lost the opportunity. Stopping operations..."
        return -1000
    pass

    #Run operations in parallel
    #t_long = threadgin.Thread(target=exchangeLong.buy, args=(currencyPair, newAskPrice, btc_amount / newAskPrice) )
    #t_short = hreadgin.Thread(target=exchangeLong.sellMargin, args=(currencyPair, newBidPrice, btc_amount / newBidPrice) )

    #Wait operations to be concluded
    #t_long.join()
    #t_short.join()

    print "secureBuy::Buy/Sell orders registered..."

    return ((newBidPrice - newAskPrice)/newAskPrice)















# Securely sell an amount of coins based on highest bid price of order book and an secure factor based on amount of coin available
#Return order to be checked or -1 if some error
# def secureSell(exchange, currencyPair, bidPrice, altcoin_amount, secureFactor=2):
#     pp = pprint.PrettyPrinter(indent=4)
#
#     if bidPrice <= 0:
#         return -1
#
#     print "Currency to sell is " + str(currencyPair.split('_')[1])
#     balance  = exchange.getBalance(currencyPair.split('_')[1])
#     if balance <= 0:
#         return -1
#
#     print "Orderbook"
#     orderBook = exchange.getOrderBook(currencyPair, 10)['bids']
#     pp.pprint(orderBook)
#
#     print "Bid Price: " + "{:.8f}".format(bidPrice) + ". Secure factor: " + str(secureFactor) + "x"
#     altcoin_volume_avaiable = 0 #Store the amount of available coins to sell converted in bitcoin
#     last_price = 0 #Check the low price on the set of possible prices to sell, improve the security of operation
#
#     for x in orderBook:
#         if float(x[0]) >= bidPrice: #Check if price is at least equal to target price
#             print "Eh maior! " + str(x[0]) + " e volume eh de: " + str(float(x[0]) * float(x[1])) + " bitcoins"
#             altcoin_volume_avaiable += float(x[0]) * float(x[1])
#             last_price = float(x[0])
#         pass
#     pass
#
#     if altcoin_volume_avaiable == 0:
#         print "No price available to sell. Probably, we lost an opportunity."
#         return -1
#     pass
#
#     print "Volume que pode ser vendido em altcoin " + str(altcoin_volume_avaiable)
#     print "Vamos checar fator de seguranca..."
#     if altcoin_volume_avaiable >= altcoin_amount * secureFactor:
#         print "Fator de seguranca alcancado, vou vender! Motivo: " + str(altcoin_volume_avaiable) + " maior que " + str(
#             altcoin_amount * secureFactor)
#         print "Sending sell order..."
#         if balance > altcoin_amount:
#             return exchange.buy(currencyPair, last_price, altcoin_amount)
#         else:
#             print "Low balance, aborting buy operation"
#             return  -1
#     else:
#         print "Fator de seguranca nao alcancado, nao vou comrpar! Motivo " + str(
#             altcoin_volume_avaiable) + " menor que " + str(
#             altcoin_amount * secureFactor)
#         return -1
#     pass
