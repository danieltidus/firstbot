import json
import pprint
import botlib
import time
import timeit
from datetime import datetime
import math
from exchanges.exchangefactory import ExchangeFactory
import utils
import logging
import ConfigParser
import telegram_send

fac = ExchangeFactory()

config = ConfigParser.RawConfigParser();
config.read('bot.cfg');
ex1 = config.get('General', 'Exchange1')
ex2 = config.get('General', 'Exchange2')

exchanges = {}

exchanges[ex1] = fac.create(ex1)
exchanges[ex2] = fac.create(ex2)

#Verify arbitrages for long/shorts combinations

spreadEntry=float(config.get('General', 'spreadEntry'))
spreadTarget=float(config.get('General', 'spreadTarget'))
simulationTime =float(config.get('General', 'simulationTime'))
btc_amount = float(config.get('General', 'btc_amount'))
orderBookFactor = float(config.get('General', 'orderBookFactor'))
#########################

combinations = botlib.findCombinations(exchanges)
print "Combinations" + str(combinations)


#Just for tests
fees = float(config.get(ex1, 'fee_maker')) + float(config.get(ex1, 'fee_taker')) + float(config.get(ex2, 'fee_maker')) + float(config.get(ex2, 'fee_taker'))
spread = {}


str_ = "log_" + datetime.now().strftime("%Y%m%d%H%M%S")
formatter = logging.Formatter('%(levelname)s:%(message)s')
logger = utils.setup_logger('main_logger', str_, formatter)

logger.info("Start simulation at %s", datetime.now().ctime())
st_ = "Exchange 1: " + ex1
logger.info(st_)
st_ = "Exchange 2: " + ex2
logger.info(st_)
st_ = "Fees na " + ex1 + " Maker: " + config.get(ex1, 'fee_maker') + " Taker: " + config.get(ex1, 'fee_taker')
logger.info(st_)
st_ = "Fees na " + ex2 + " Maker: " + config.get(ex2, 'fee_maker') + " Taker: " + config.get(ex2, 'fee_taker')
logger.info(st_)
st_ = "Total fees: " + str(fees)
logger.info(st_)
st_ = "spreadEntry: " + config.get('General', 'spreadEntry')
logger.info(st_)
st_ = "spreadTarget: " + config.get('General', 'spreadTarget')
logger.info(st_)
st_ = "simulationTime: " +config.get('General', 'simulationTime')
logger.info(st_)
st_ = "BTC amount: " + config.get('General', 'btc_amount')
logger.info(st_)
st_ = "Order Book Factor: " + config.get('General', 'orderBookFactor')
logger.info(st_)
logger.info("")

spreadExit = {}
profitCount = {}

#Loading state if exist and user wanna load.
if utils.hasSavedState(exchanges[ex1].getExchangeName(), exchanges[ex2].getExchangeName()):
    # Setting up state
    ok = False
    ans = ""
    while(ok == False):
        print "There is a state file with data stored for this combination of exchanges!"
        print "Do you want to load this state?"
        ans = raw_input('Choose s (sim) or n (nao): ')
        if ans == "s" or ans == "n":
            ok = True

    if ans == "s":
        spreadExit = utils.loadStateSpread(ex1, ex2)
        profitCount = utils.loadProfitCount(ex1, ex2)
pass

if len(profitCount) == 0:
    for c in combinations:
        profitCount[c["id"]] = 0
        pass
pass

#Just to send informations each hour
time_ticker = timeit.default_timer()
telegram_send.send(['Firsbot Ping: We are starting at ' + str(datetime.now().ctime())])

while 1:
    start = timeit.default_timer()
    delta_time = start - time_ticker
    #Looking entry opportunities
    for c in combinations:

        if not (c["id"] in spreadExit): #If not already ON Market

            #print "Get Balance long..."
            balanceLong = exchanges[c["LongEx"]].getBalance('BTC')
            #print "Get Balance short..."
            balanceShort = exchanges[c["ShortEx"]].getBalance('BTC')

            priceLong = exchanges[c["LongEx"]].getAsk(c["pair"])
            priceShort = exchanges[c["ShortEx"]].getBid(c["pair"])

            if (priceLong > 0.0 and priceShort > 0.0):
                spread[c["id"]] = (priceShort - priceLong) / priceLong
            else:
                spread[c["id"]] = 0.0
            pass

            str_ = "[ " + str(datetime.now().ctime()) + " ] " + "Spread in for pair " + c["pair"] + " is " + str(round(spread[c["id"]]*100,2)) + " %"
            logger.info(str_)
            if spread[c["id"]] >= spreadEntry: #TODO chekEntry-like process checkEntry(c["id"], priceLong, princeShort, spread, spreadEntry)
                logger.info("[ %s ] We found a arbitrage opportunity", datetime.now().ctime())




                #TODO Inserting code to secure get inside the arbitrage
                realSpread = botlib.secureIn(exchanges[c["LongEx"]], exchanges[c["ShortEx"]], balanceLong, balanceShort, c["pair"],
                         priceLong, priceShort, btc_amount, orderBookFactor, spreadEntry)
                if realSpread != -1000 and realSpread != -1001:
                    logger.info("[ %s ] Everything ok! Arbitrage opportunity explored!", datetime.now().ctime())
                    spreadExit[c["id"]] = realSpread - spreadTarget - fees
                    utils.addState(ex1, ex2, c["id"], c["pair"], spreadExit[c["id"]])
                else:
                    if realSpread == -1001:
                        logger.info(" [ %s ] Arbitrage opportunity not explored. Some problem on buy/sell operations. you should revert (TODO)!", datetime.now().ctime())
                    else:
                        logger.info(" [ %s ] Arbitrage opportunity not explored.", datetime.now().ctime())
            pass




        else: #Looking exit opportunities

            priceLong = exchanges[c["LongEx"]].getBid(c["pair"])
            priceShort = exchanges[c["ShortEx"]].getAsk(c["pair"])

            if (priceLong > 0.0 and priceShort > 0.0):
                spread[c["id"]] = (priceShort - priceLong) / priceLong
            else:
                spread[c["id"]] = 0.0
            pass

            str_ = "[ " + str(datetime.now().ctime()) + " ] " + "Pair " + c["pair"] + " with LongEx " + c["LongEx"] + " and ShortEx " + c["ShortEx"] + " ON Market"
            logger.info(str_)
            str_ = "[ " + str(datetime.now().ctime()) + " ] " + "Current spread " + str(round(spread[c["id"]]*100,2)) + " and target spread to exit " + str(round(spreadExit[c["id"]]*100,2))
            logger.info(str_)
            if spread[c["id"]] <= spreadExit[c["id"]]: #TODO checkExit-like process
                str_ = "[ " + str(datetime.now().ctime()) + " ] " + "We found a exit opportunity for pair " + c["pair"]
                logger.info(str_)

                # TODO Code to sell the asset e possible made profit;
                str_pair = c["pair"].split('_')
                print "Splitting ..." + str_pair[0] + " " + str_pair[1]


                balanceLongAltCoin = exchanges[c["LongEx"]].getBalance(str_pair[1])
                balanceShortAltCoin = exchanges[c["ShortEx"]].getMarginBalance(c["pair"])
                print "balanceLongAltCoin: " + str(balanceLongAltCoin) + " balanceShortAltCoin: " + str(balanceShortAltCoin)

                realSpread = botlib.secureOut(exchanges[c["LongEx"]], exchanges[c["ShortEx"]], balanceLongAltCoin, balanceShortAltCoin, c["pair"], priceLong,
                          priceShort, orderBookFactor, spreadExit[c["id"]])

                if realSpread != -1000 and realSpread != -1001:
                    logger.info(" [ %s ] Everything ok! Arbitrage opportunity completed. Probably we make profit!", datetime.now().ctime())
                    # INFO here are log info. Maybe remove this after
                    str_ = "[ " + str(datetime.now().ctime()) + " ] " + "We made " + str(spreadTarget * 100) + "% of profit!"
                    logger.info(str_)
                    spreadExit.pop(c["id"])
                    utils.removeState(ex1, ex2, c["id"])
                    profitCount[c["id"]] = profitCount[c["id"]] + 1
                    utils.updateStateofCounters(ex1, ex2, combinations, profitCount)
                else:
                    if realSpread == -1001:
                        logger.info(
                            " [ %s ] Arbitrage opportunity not explored. Some problem on buy/sell operations. you should revert (TODO)!",
                            datetime.now().ctime())
                    else:
                        logger.info(" [ %s ] Arbitrage exit opportunity not explored.", datetime.now().ctime())


            pass
    pass

    logger.info("[ %s ] Simulation resume", datetime.now().ctime())
    logger.info("[ %s ] Profit count for earch pair", datetime.now().ctime())

    for c in combinations:
        str_ = "[ " + str(datetime.now().ctime()) + " ] " + "Times that profit occurs on pair " + c["pair"] + ": " + str(profitCount[c["id"]])
        logger.info(str_)
        pass

    logger.info("\n")

    if delta_time >= 3600:
        time_ticker = timeit.default_timer()
        telegram_send.send(['Firsbot Ping: We are alive at ' + str(datetime.now().ctime())])

    stop =  timeit.default_timer()
    time.sleep(math.fabs(simulationTime - round(stop - start)))
pass
