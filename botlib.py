import pprint
from multiprocessing.pool import ThreadPool
from datetime import datetime

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


    print "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "] Balance on long exchange " + str(balanceLong)
    print "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "] Balance on short exchange " + str(balanceShort)
    #No need balance available
    if balanceLong <= btc_amount or balanceShort <= btc_amount:
        print "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "] No balance available. Verify long and short exchanges balance."
        return -1000

    print "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "] Orderbook"
    orderBookLong = exchangeLong.getOrderBook(currencyPair, 'asks', 10)
    orderBookShort = exchangeShort.getOrderBook(currencyPair, 'bids', 10)

    print "Orderbook Long..."
    pp.pprint(orderBookLong)
    print "Orderbook Short..."
    pp.pprint(orderBookShort)

    print "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "] Ask Price: " + "{:.8f}".format(askPrice) + ". Secure factor: " + str(secureFactor) + "x"
    print "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "] Bid Price: " + "{:.8f}".format(bidPrice) + ". Secure factor: " + str(secureFactor) + "x"

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

    print "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "]  New Ask price " + str(newAskPrice)
    print "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "]  New Bid price " + str(newBidPrice)

    #Verify if we have error with new prices
    if newAskPrice == 0.0 or newBidPrice == 0.0:
        print "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "] Something wrong with order books. Stopping operations..."
        return -1000
    pass

    print "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "]  BTC Amount available on Long " + str(btc_volume_avaiable_long)
    print "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "]  BTC Amount available on short " + str(btc_volume_avaiable_short)
    # Verify if we have errors with liquidity
    if btc_volume_avaiable_long < btc_amount*secureFactor or btc_volume_avaiable_short < btc_amount*secureFactor:
        print "secureIn::[" + str(currencyPair) + "] Not enough liquidity. Stopping operations..."
        return -1000
    pass

    print "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "]  Current Spread " + str(spreadTarget)
    print "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "]  New Spread " +  "{:.8f}".format(((newBidPrice - newAskPrice)/newAskPrice))

    # Verify if we have error with spreadTarget
    if spreadTarget > ((newBidPrice - newAskPrice)/newAskPrice):
        print "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "] Invalid new spread. We lost the opportunity. Stopping operations..."
        return -1000
    pass

    pool = ThreadPool(processes=2)

    print "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "] Calling buy thread on long operation..."
    async_result_long = pool.apply_async(exchangeLong.buy, (currencyPair, newAskPrice, btc_amount / newAskPrice)) # tuple of args for foo
    print "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "] Calling buy thread on short operation..."
    async_result_short = pool.apply_async(exchangeLong.sellMargin, (currencyPair, newBidPrice, btc_amount / newBidPrice)) # tuple of args for foo


    print "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "] Waiting operations to be completed..."


    order_long = async_result_long.get()  # get the return value from your function.
    order_short = async_result_short.get()  # get the return value from your function.

    if order_long == -1 or order_short == -1:
        print "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "] Problem on buy/sell operation. Buy order is: " + str(order_long) + ". Sell order is: " + str(order_short) +"."
        #TODO: Revert operations that occurred and the other one not.
        return -1001
    else:
        print "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "] Buy/Sell orders registered..."
        return ((newBidPrice - newAskPrice)/newAskPrice)







# Securely buy/sell an amount of coins based on lowest ask price of order book and an secure factor based on amount of coin available
#Return order to be checked or -1 if some error
def secureOut(exchangeLong, exchangeShort, balanceLongAltCoin, balanceShortAltCoin, currencyPair, longPrice, shortPrice, secureFactor=2, spreadTarget=-0.0008):
    pp = pprint.PrettyPrinter(indent=4)

    if longPrice <= 0 or shortPrice <=0:
        return -1000

    print "secureOut::[" + str(currencyPair) + "] Balance on long altcoin exchange " + str(balanceLongAltCoin)
    print "secureOut::[" + str(currencyPair) + "] Balance on short altcoin exchange " + str(balanceShortAltCoin)
    #No need balance available
    if balanceLongAltCoin <= 0 or balanceShortAltCoin <= 0:
        print "secureOut::[" + str(currencyPair) + "] No balance available. Verify long and short exchanges balance."
        return -1000

    # We invert, cause we will make opposit operations. Go selling on longExchange and buying on ShortExchange
    print "secureOut::[" + str(currencyPair) + "] Orderbook"
    orderBookLong = exchangeLong.getOrderBook(currencyPair, 'bids', 10) #
    orderBookShort = exchangeShort.getOrderBook(currencyPair, 'asks', 10) # We invert, cause we will make opposit operations

    print "Orderbook Long..."
    pp.pprint(orderBookLong)
    print "Orderbook Short..."
    pp.pprint(orderBookShort)

    print "secureOut::[" + str(currencyPair) + "] Long Price: " + "{:.8f}".format(longPrice) + ". Secure factor: " + str(secureFactor) + "x"
    print "secureOut::[" + str(currencyPair) + "] Short Price: " + "{:.8f}".format(shortPrice) + ". Secure factor: " + str(secureFactor) + "x"

    altcoin_volume_avaiable_long = 0  # Store the amount of available coins to buy converted in bitcoin
    altcoin_volume_avaiable_short = 0  # Store the amount of available coins to sell converted in bitcoin
    newLongPrice = 0.0
    newShortPrice = 0.0

    #Calculating liquidity in each book
    for x in orderBookLong:
        altcoin_volume_avaiable_long += float(x[1])
        newLongPrice = float(x[0])
        if altcoin_volume_avaiable_long >= balanceLongAltCoin*secureFactor:
            break
        pass
    pass

    for x in orderBookShort:
        altcoin_volume_avaiable_short += float(x[1])
        newShortPrice = float(x[0])
        if altcoin_volume_avaiable_short >= balanceShortAltCoin*secureFactor:
            break
        pass
    pass

    print "secureOut::[" + str(currencyPair) + "]  New Long price " + str(newLongPrice)
    print "secureOut::[" + str(currencyPair) + "]  New Short price " + str(newShortPrice)

    #Verify if we have error with new prices
    if newLongPrice == 0.0 or newShortPrice == 0.0:
        print "secureOut::[" + str(currencyPair) + "] Something wrong with order books. Stopping operations..."
        return -1000
    pass

    print "secureOut::[" + str(currencyPair) + "]  Altcoin Amount available on Long " + str(altcoin_volume_avaiable_long)
    print "secureOut::[" + str(currencyPair) + "]  Altcoin Amount available on short " + str(altcoin_volume_avaiable_short)
    # Verify if we have errors with liquidity
    if altcoin_volume_avaiable_long < balanceLongAltCoin*secureFactor or altcoin_volume_avaiable_short < balanceShortAltCoin*secureFactor:
        print "secureOut::[" + str(currencyPair) + "] Not enough liquidity. Stopping operations..."
        return -1000
    pass

    print "secureOut::[" + str(currencyPair) + "]  Current Spread " + str(spreadTarget)
    print "secureOut::[" + str(currencyPair) + "]  New Spread " +  "{:.8f}".format(((newShortPrice - newLongPrice)/newLongPrice))

    # Verify if we have error with spreadTarget
    if spreadTarget < ((newShortPrice - newLongPrice)/newLongPrice):
        print "secureOut::[" + str(currencyPair) + "] Invalid new spread. We lost the opportunity. Stopping operations..."
        return -1000
    pass

    #Run operations in parallel
    #t_long = threading.Thread(target=exchangeLong.sell, args=(currencyPair, newLongPrice, balanceLongAltCoin) )
    #t_short = threading.Thread(target=exchangeLong.buyMargin, args=(currencyPair, newShortPrice, balanceShortAltCoin) )

    #Wait operations to be concluded
    #t_long.join()
    #t_short.join()

    print "secureOut::[" + str(currencyPair) + "] Sell/buyMargin orders registered..."

    return ((newShortPrice - newLongPrice)/newLongPrice)
