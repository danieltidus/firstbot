import json
import pprint
import botlib;
import time;
import timeit;
from datetime import datetime
import math;
import logging;
from exchanges.exchangefactory import ExchangeFactory


fac = ExchangeFactory()

exchanges = {}
exchanges['Poloniex'] = fac.create('Poloniex')
exchanges['Bittrex'] = fac.create('Bittrex')

#Verify arbitrages for long/shorts combinations
#Parameters - TODO Put on config file;
spreadEntry=0.0080
spreadTarget=0.0050
simulationTime = 10.0 #simulation time in seconds
#########################

spreadExit = [];
combinations = botlib.findCombinations(exchanges)
print combinations

print exchanges['Bittrex'].getBid("BTC_ETH")
print exchanges['Bittrex'].getAsk("BTC_LTC")
#Just for tests
fees = 0.0090
spread = {}
spreadExit = {}
profitCount = {}

for c in combinations:
    profitCount[c["id"]] = 0
    pass

print profitCount

str_ = "log_" + datetime.now().strftime("%Y%m%d%H%M%S")
logging.basicConfig(filename=str_, format='%(levelname)s:%(message)s', level=logging.INFO)
logging.info("Start simulation at %s", datetime.now().ctime())
logging.info("")
logging.info("")

while 1:
    start = timeit.default_timer()
    #Looking entry opportunities

    #print "Get Balance long..."
    balanceLong = exchanges['Bittrex'].getBalance('BTC')
    #print "Get Balance short..."
    balanceShort = exchanges['Poloniex'].getBalance('BTC')


    for c in combinations:


        if not (c["id"] in spreadExit): #If not already ON Market

            priceLong = exchanges[c["LongEx"]].getAsk(c["pair"])
            priceShort = exchanges[c["ShortEx"]].getBid(c["pair"])

            if (priceLong > 0.0 and priceShort > 0.0):
                spread[c["id"]] = (priceShort - priceLong) / priceLong
            else:
                spread[c["id"]] = 0.0
            pass

            str_ = "Spread in for pair " + c["pair"] + " is " + str(round(spread[c["id"]]*100,2)) + " %"
            logging.info(str_);
            if spread[c["id"]] >= spreadEntry: #TODO chekEntry-like process checkEntry(c["id"], priceLong, princeShort, spread, spreadEntry)
                logging.info("We found a arbitrage opportunity")




                #TODO Inserting code to secure get inside the arbitrage
                realSpread = botlib.secureIn(exchanges[c["LongEx"]], exchanges[c["ShortEx"]], balanceLong, balanceShort, c["pair"],
                         priceLong, priceShort, 0.02, 2, spreadEntry)
                if realSpread != -1000:
                    logging.info("Everything ok! Arbitrage opportunity explored!")
                    spreadExit[c["id"]] = realSpread - spreadTarget - fees
                else:
                    logging.info("Arbitrage opportunity not explored")



            pass
        else: #Looking exit opportunities

            priceLong = exchanges[c["LongEx"]].getBid(c["pair"])
            priceShort = exchanges[c["ShortEx"]].getAsk(c["pair"])

            if (priceLong > 0.0 and priceShort > 0.0):
                spread[c["id"]] = (priceShort - priceLong) / priceLong
            else:
                spread[c["id"]] = 0.0
            pass

            str_ = "Pair " + c["pair"] + " with LongEx " + c["LongEx"] + " and ShortEx " + c["ShortEx"] + " ON Market"
            logging.info(str_)
            str_ = "Current spread " + str(round(spread[c["id"]]*100,2)) + " and target spread to exit " + str(round(spreadExit[c["id"]]*100,2))
            logging.info(str_)
            if spread[c["id"]] <= spreadExit[c["id"]]: #TODO checkExit-like process
                str_ = "We found a exit opportunity for pair " + c["pair"]
                logging.info(str_)

                # TODO Code to sell the asset e possible made profit;
                str_pair = c["pair"].split('_')
                print "Splitting ..." + str_pair[0] + " " + str_pair[1]


                balanceLongAltCoin = exchanges[c["LongEx"]].getBalance(str_pair[0])
                balanceShortAltCoin = exchanges[c["ShortEx"]].getMarginBalance(str_pair[1])
                print "balanceLongAltCoin: " + str(balanceLongAltCoin) + " balanceShortAltCoin: " + str(balanceShortAltCoin)

                realSpread = secureOut(exchanges[c["LongEx"]], exchanges[c["ShortEx"]], balanceLongAltCoin, balanceShortAltCoin, c["pair"], priceLong,
                          priceShort, 2, spreadExit[c["id"]])

                if realSpread != -1000:
                    logging.info("Everything ok! Arbitrage opportunity completed. Probably we make profit!")
                    # INFO here are log info. Maybe remove this after
                    str_ = "We made " + str(spreadTarget * 100) + "% of profit!"
                    logging.info(str_)
                    spreadExit.pop(c["id"])
                    profitCount[c["id"]] = profitCount[c["id"]] + 1
                else:
                    logging.info("Arbitrage opportunity to exit not explored")


            pass
    pass

    print

    logging.info("Simulation resume")
    logging.info("Profit count for earch pair")

    for c in combinations:
        str_ = "Times that profit occurs on pair " + c["pair"] + ": " + str(profitCount[c["id"]])
        logging.info(str_)
        pass

    logging.info("\n")

    stop =  timeit.default_timer()
    time.sleep(math.fabs(simulationTime - round(stop - start)))
pass
