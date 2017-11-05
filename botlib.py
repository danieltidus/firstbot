import pprint
from multiprocessing.pool import ThreadPool
from datetime import datetime
import time
import utils
import logging
import telegram_send

str_ = "control_" + datetime.now().strftime("%Y%m%d%H%M%S")
formatter = logging.Formatter('%(levelname)s:%(message)s')
logger = utils.setup_logger('botlib_logger', str_, formatter)


# Receive a dict vector of exchanges and return a array of combinations
def findCombinations(exchanges={}):
    # Find possible combinations of short and long on exchanges
    pairsByExchange = {}
    combinations = []

    for ex in exchanges:
        st_ = "Get LongShortPairs to exchange: " + exchanges[ex].getExchangeName();
        logger.info(st_)
        pairsByExchange[exchanges[ex].getExchangeName()] = exchanges[ex].getLongShortPairs();

        # st_ = "Long short to " + exchanges[ex].getExchangeName()
        # st_ = pairsByExchange[exchanges[ex].getExchangeName()]
        # st_ = "\n\n\n\n"
        pass
    id_ = 0
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
# Return order to be checked or -1 if some error
def secureIn(exchangeLong, exchangeShort, balanceLong, balanceShort, currencyPair, askPrice, bidPrice, btc_amount=0.02,
             secureFactor=2, spreadTarget=-0.0008):
    pp = pprint.PrettyPrinter(indent=4)

    if askPrice <= 0 or bidPrice <= 0:
        return -1000

    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
        currencyPair) + "] Balance on long exchange " + str(balanceLong)
    logger.info(st_)
    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
        currencyPair) + "] Balance on short exchange " + str(balanceShort)
    logger.info(st_)
    # No need balance available
    if balanceLong <= btc_amount or balanceShort <= btc_amount:
        st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
            currencyPair) + "] No balance available. Verify long and short exchanges balance."
        return -1000

    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "] Orderbook"
    logger.info(st_)
    orderBookLong = exchangeLong.getOrderBook(currencyPair, 'asks', 10)
    orderBookShort = exchangeShort.getOrderBook(currencyPair, 'bids', 10)

    st_ = "Orderbook Long..."
    logger.info(st_)
    logger.info(orderBookLong)
    #pp.pprint(orderBookLong)
    st_ = "Orderbook Short..."
    logger.info(st_)
    logger.info(orderBookShort)
    #pp.pprint(orderBookShort)

    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
        currencyPair) + "] Ask Price: " + "{:.8f}".format(askPrice) + ". Secure factor: " + str(secureFactor) + "x"
    logger.info(st_)
    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
        currencyPair) + "] Bid Price: " + "{:.8f}".format(bidPrice) + ". Secure factor: " + str(secureFactor) + "x"
    logger.info(st_)

    btc_volume_avaiable_long = 0  # Store the amount of available coins to buy converted in bitcoin
    btc_volume_avaiable_short = 0  # Store the amount of available coins to sell converted in bitcoin
    newAskPrice = 0.0
    newBidPrice = 0.0

    # Calculating liquidity in each book
    for x in orderBookLong:
        btc_volume_avaiable_long += float(x[0]) * float(x[1])
        newAskPrice = float(x[0])
        if btc_volume_avaiable_long >= btc_amount * secureFactor:
            break
        pass
    pass

    btc_volume_avaiable = 0
    for x in orderBookShort:
        btc_volume_avaiable_short += float(x[0]) * float(x[1])
        newBidPrice = float(x[0])
        if btc_volume_avaiable_short >= btc_amount * secureFactor:
            break
        pass
    pass

    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "]  New Ask price " + str(
        newAskPrice)
    logger.info(st_)
    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "]  New Bid price " + str(
        newBidPrice)
    logger.info(st_)

    # Verify if we have error with new prices
    if newAskPrice == 0.0 or newBidPrice == 0.0:
        st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
            currencyPair) + "] Something wrong with order books. Stopping operations..."
        logger.info(st_)
        return -1000
    pass

    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
        currencyPair) + "]  BTC Amount available on Long " + str(btc_volume_avaiable_long)
    logger.info(st_)
    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
        currencyPair) + "]  BTC Amount available on short " + str(btc_volume_avaiable_short)
    logger.info(st_)

    # Verify if we have errors with liquidity
    if btc_volume_avaiable_long < btc_amount * secureFactor or btc_volume_avaiable_short < btc_amount * secureFactor:
        st_ = "secureIn::[" + str(currencyPair) + "] Not enough liquidity. Stopping operations..."
        logger.info(st_)

        return -1000
    pass

    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "]  Current Spread " + str(
        spreadTarget)
    logger.info(st_)
    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
        currencyPair) + "]  New Spread " + "{:.8f}".format(((newBidPrice - newAskPrice) / newAskPrice))
    logger.info(st_)

    # Verify if we have error with spreadTarget
    if spreadTarget > ((newBidPrice - newAskPrice) / newAskPrice):
        st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
            currencyPair) + "] Invalid new spread. We lost the opportunity. Stopping operations..."
        logger.info(st_)

        return -1000
    pass

    pool = ThreadPool(processes=2)

    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
        currencyPair) + "] Calling buy thread on long operation..."
    logger.info(st_)
    async_result_long = pool.apply_async(exchangeLong.buy,
                                         (currencyPair, newAskPrice, btc_amount / newAskPrice))  # tuple of args for foo
    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
        currencyPair) + "] Calling sellMargin thread on short operation..."
    logger.info(st_)
    async_result_short = pool.apply_async(exchangeShort.sellMargin, (
    currencyPair, newBidPrice, btc_amount / newBidPrice))  # tuple of args for foo

    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
        currencyPair) + "] Waiting operations to be completed..."
    logger.info(st_)

    order_long = async_result_long.get()  # get the return value from your function.
    order_short = async_result_short.get()  # get the return value from your function.

    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
        currencyPair) + "] Waiting more to ensure order complete...."
    logger.info(st_)
    time.sleep(5)

    altcoin = currencyPair.split('_')[1]

    altlong = exchangeLong.getBalance(altcoin)
    altshort = exchangeShort.getMarginBalance(currencyPair)


    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
        currencyPair) + "] Altcoin balance on long " + str(altlong) + " Altcoin balance on short " + str(altshort)
    logger.info(st_)


    if order_long == -1 or order_short == -1:
        st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
            currencyPair) + "] Problem buying/selling Status order long " + str(order_long) + " Status order " + str(order_short)
        logger.info(st_)
        msg = st_
        st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
            currencyPair) + "] Stopping bot, sorry! :'("
        logger.info(st_)
        msg = msg + "\n" + st_
        #utils.sendmail('Bot Sucess on SecureOut', msg)
        telegram_send.send([msg])
        exit(-1)

    complete = False
    while complete == False:
        openLong = exchangeLong.hasOpenOrder(currencyPair)
        openShort = exchangeShort.hasOpenOrder(currencyPair)
        if openLong == True or openShort == True:
            st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
                currencyPair) + "] Uncompleted orders, waiting... (Sleppage???). Status long: " + str(openLong) + " Status short: " + str(openShort)
            logger.info(st_)
            time.sleep(2)
        else:
            st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
                currencyPair) + "] Orders completed!!!!"
            logger.info(st_)
            complete = True

    # if order_long == -1 or order_short == -1 or altlong <= 0.0 or altshort <= 0.0:
    #     st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
    #         currencyPair) + "] Problem on buy/sell operation. Buy order is: " + str(
    #         order_long) + ". Sell order is: " + str(order_short) + "."
    #     logger.info(st_)
    #     st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
    #         currencyPair) + "] Closing short positions..."
    #     logger.info(st_)
    #     res = exchangeShort.closeMarginPosition(currencyPair)
    #     if res == -1:
    #         st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
    #             currencyPair) + "] Warning if alt balances different of zero, otherwise calm down! Reverting short operation. Houston, we have a problem!"
    #         logger.info(st_)
    #
    #     res = exchangeLong.closeAllPositions(currencyPair)
    #     if res == -1:
    #         st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
    #             currencyPair) + "] Warning if alt balances different of zero, otherwise calm down! Reverting long operation. Houston, we have a problem!"
    #         logger.info(st_)
    #
    #     return -1000
    # else:
    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(currencyPair) + "] Buy/Sell orders ok..."
    logger.info(st_)
    #utils.sendmail('Bot Sucess on SecureIn', st_)
    telegram_send.send([st_])
    return ((newBidPrice - newAskPrice) / newAskPrice)


# Securely buy/sell an amount of coins based on lowest ask price of order book and an secure factor based on amount of coin available
# Return order to be checked or -1 if some error
def secureOut(exchangeLong, exchangeShort, balanceLongAltCoin, balanceShortAltCoin, currencyPair, longPrice, shortPrice,
              secureFactor=2, spreadTarget=-0.0008):
    pp = pprint.PrettyPrinter(indent=4)

    if longPrice <= 0 or shortPrice <= 0:
        return -1000

    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(
        currencyPair) + "] Balance on long altcoin exchange " + str(balanceLongAltCoin)
    logger.info(st_)
    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(
        currencyPair) + "] Balance on short altcoin exchange " + str(balanceShortAltCoin)
    logger.info(st_)
    # No need balance available
    if balanceLongAltCoin <= 0 or balanceShortAltCoin <= 0:
        st_ = "secureOut::[" + str(currencyPair) + "] No balance available. Verify long and short exchanges balance."
        logger.info(st_)
        return -1000

    # We invert, cause we will make opposit operations. Go selling on longExchange and buying on ShortExchange
    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(currencyPair) + "] Orderbook"
    logger.info(st_)
    orderBookLong = exchangeLong.getOrderBook(currencyPair, 'bids', 10)  #
    orderBookShort = exchangeShort.getOrderBook(currencyPair, 'asks',
                                                10)  # We invert, cause we will make opposit operations

    st_ = "Orderbook Long..."
    logger.info(st_)
    logger.info(orderBookLong)
    # pp.pprint(orderBookLong)
    st_ = "Orderbook Short..."
    logger.info(st_)
    logger.info(orderBookShort)
    # pp.pprint(orderBookShort)

    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(
        currencyPair) + "] Long Price: " + "{:.8f}".format(longPrice) + ". Secure factor: " + str(secureFactor) + "x"
    logger.info(st_)
    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(
        currencyPair) + "] Short Price: " + "{:.8f}".format(shortPrice) + ". Secure factor: " + str(secureFactor) + "x"
    logger.info(st_)

    altcoin_volume_avaiable_long = 0  # Store the amount of available coins to buy converted in bitcoin
    altcoin_volume_avaiable_short = 0  # Store the amount of available coins to sell converted in bitcoin
    newLongPrice = 0.0
    newShortPrice = 0.0

    # Calculating liquidity in each book
    for x in orderBookLong:
        altcoin_volume_avaiable_long += float(x[1])
        newLongPrice = float(x[0])
        if altcoin_volume_avaiable_long >= balanceLongAltCoin * secureFactor:
            break
        pass
    pass

    for x in orderBookShort:
        altcoin_volume_avaiable_short += float(x[1])
        newShortPrice = float(x[0])
        if altcoin_volume_avaiable_short >= balanceShortAltCoin * secureFactor:
            break
        pass
    pass

    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(currencyPair) + "]  New Long price " + str(
        newLongPrice)
    logger.info(st_)
    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(currencyPair) + "]  New Short price " + str(
        newShortPrice)
    logger.info(st_)

    # Verify if we have error with new prices
    if newLongPrice == 0.0 or newShortPrice == 0.0:
        st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(
            currencyPair) + "] Something wrong with order books. Stopping operations..."
        logger.info(st_)
        return -1000
    pass

    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(
        currencyPair) + "]  Altcoin Amount available on Long " + str(altcoin_volume_avaiable_long)
    logger.info(st_)
    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(
        currencyPair) + "]  Altcoin Amount available on short " + str(altcoin_volume_avaiable_short)
    logger.info(st_)

    # Verify if we have errors with liquidity
    if altcoin_volume_avaiable_long < balanceLongAltCoin * secureFactor or altcoin_volume_avaiable_short < balanceShortAltCoin * secureFactor:
        st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(
            currencyPair) + "] Not enough liquidity. Stopping operations..."
        logger.info(st_)
        return -1000
    pass

    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(currencyPair) + "]  Current Spread " + str(
        spreadTarget)
    logger.info(st_)
    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(
        currencyPair) + "]  New Spread " + "{:.8f}".format(((newShortPrice - newLongPrice) / newLongPrice))
    logger.info(st_)

    # Verify if we have error with spreadTarget
    if spreadTarget < ((newShortPrice - newLongPrice) / newLongPrice):
        st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(
            currencyPair) + "] Invalid new spread. We lost the exit opportunity. Stopping operations..."
        logger.info(st_)
        return -1000
    pass

    pool = ThreadPool(processes=2)

    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(
        currencyPair) + "] Calling sell thread on long operation..."
    logger.info(st_)
    async_result_long = pool.apply_async(exchangeLong.sell,
                                         (currencyPair, newLongPrice, balanceLongAltCoin))  # tuple of args for foo
    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(
        currencyPair) + "] Calling buyMargin thread on short operation..."
    logger.info(st_)
    async_result_short = pool.apply_async(exchangeShort.buyMargin,
                                          (currencyPair, newShortPrice, balanceShortAltCoin))  # tuple of args for foo

    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(
        currencyPair) + "] Waiting operations to be completed..."
    logger.info(st_)

    order_long = async_result_long.get()  # get the return value from your function.
    order_short = async_result_short.get()  # get the return value from your function.


    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(
        currencyPair) + "] Waiting more to ensure order complete...."
    logger.info(st_)
    time.sleep(5)

    altcoin = currencyPair.split('_')[1]

    altlong = exchangeLong.getBalance(altcoin)
    altshort = exchangeShort.getMarginBalance(currencyPair)
    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(
        currencyPair) + "] Altcoin balance on long " + str(altlong) + "Alcoin balance on short " + str(altshort)
    logger.info(st_)


    if order_long == -1 or order_short == -1:
        st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(
            currencyPair) + "] Problem buying/selling Status order long " + str(order_long) + " Status order " + str(order_short)
        logger.info(st_)
        msg = st_
        st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(
            currencyPair) + "] Stopping bot, sorry! :'("
        logger.info(st_)
        msg = msg + "\n"+st_
        #utils.sendmail('Bot fail', msg)
        telegram_send.send([msg])
        exit(-1)

    complete = False
    while complete == False:
        openLong = exchangeLong.hasOpenOrder(currencyPair)
        openShort = exchangeShort.hasOpenOrder(currencyPair)
        if openLong == True or openShort == True:
            st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(
                currencyPair) + "] Uncompleted orders, waiting... (Sleppage???). Status long: " + str(openLong) + " Status short: " + str(openShort)
            logger.info(st_)
            time.sleep(2)
        else:
            st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(
                currencyPair) + "] Orders completed!!!!"
            logger.info(st_)
            complete = True

    #Just to close some trash values that resist on short position
    res = exchangeShort.closeMarginPosition(currencyPair)
    if res == -1:
        st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(
            currencyPair) + "] FATAL ERROR completing operation closeMarginPosition. Houston, we have a problem!"
        logger.info(st_)
        #utils.sendmail('Bot fail', st_)
        telegram_send.send([st_])
        exit(-1)
    pass


    #
    # ok = False
    # if order_long != -1 and order_short != -1:
    #     ok = True
    #
    # count = 1
    # while ok == False:
    #     st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(
    #         currencyPair) + "] Problem selling/buying. Trying again... Attempt #" + str(count)
    #     logger.info(st_)
    #
    #     if order_long == -1:
    #         order_long = exchangeLong.sell(currencyPair, newLongPrice, balanceLongAltCoin)
    #     if order_short == -1:
    #         order_short = exchangeShort.buyMargin(currencyPair, newShortPrice, balanceShortAltCoin)
    #     if order_long != -1 and order_short != -1:
    #         ok = True
    #     time.sleep(1)
    #     count = count + 1
    # pass

    #
    # if altlong != 0.0:
    #     if altlong != -1:
    #         st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
    #             currencyPair) + "] Problems on long so trying to complete operation"
    #         logger.info(st_)
    #         res = exchangeLong.closeAllPositions(currencyPair)
    #         if res == -1:
    #             st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
    #                 currencyPair) + "] FATAL ERROR completing operation. Houston, we have a problem!"
    #             logger.info(st_)
    #         pass
    #     else:
    #         st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
    #             currencyPair) + "] Error accessing altcoin balance on long"
    #
    # if altshort != 0.0:
    #     if altshort != -1:
    #         st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
    #             currencyPair) + "] Problems on short so trying to complete operation"
    #         logger.info(st_)
    #         res = exchangeShort.closeMarginPosition(currencyPair)
    #         if res == -1:
    #             st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
    #                 currencyPair) + "] FATAL ERROR completing operation. Houston, we have a problem!"
    #             logger.info(st_)
    #         pass
    #     else:
    #         st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureIn::[" + str(
    #             currencyPair) + "] Error accessing altcoin balance on short"

    msg = ""
    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut::[" + str(
        currencyPair) + "] Sell/BuyMargin orders ok..."
    logger.info(st_)
    msg = msg + st_
    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut:: BTC Value gained on LongEx: " + str(
        exchangeLong.getOrderBTCValue(order_long))
    logger.info(st_)
    msg = msg + "\n" + st_
    st_ = "[ " + str(datetime.now().ctime()) + " ] " + "secureOut:: BTC Value gained on ShortEx: " + str(
        exchangeShort.getOrderBTCValue(order_short))
    logger.info(st_)
    msg = msg + "\n" + st_
    #utils.sendmail('Bot Sucess on SecureOut', msg)
    telegram_send.send([msg])
    return (newShortPrice - newLongPrice) / newLongPrice
