

#Receive a dict vector of exchanges and return a array of combinations
def findCombinations(exchanges = {}):
    #Find possible combinations of short and long on exchanges
    pairsByExchange = {};
    combinations = [];

    for ex in exchanges:
        print "Get LongShortPairs to exchange: " + exchanges[ex].getExchangeName();
        pairsByExchange[exchanges[ex].getExchangeName()] = exchanges[ex].getLongShortPairs();
        pass
    id_ = 0;
    for ex in pairsByExchange:
        for pair_on_long in pairsByExchange[ex]["LONG"]:
            for other_ex in pairsByExchange:
                if other_ex != ex:
                    for pair_on_short in pairsByExchange[other_ex]["SHORT"]:

                        if (pair_on_short == pair_on_long):
                            if pairsByExchange[other_ex]["SHORT"][pair_on_short] == pairsByExchange[ex]["LONG"][pair_on_long]:
                                str_pair = pairsByExchange[other_ex]["SHORT"][pair_on_short]+"_"+pair_on_short;
                                combinations.append({'id': id_, 'pair':str_pair, 'LongEx':ex, 'ShortEx':other_ex});
                                id_ = id_ + 1;
                            pass

                        pass
                    pass
                pass
            pass
        pass
    pass

    return combinations;
