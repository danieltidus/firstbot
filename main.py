import json
import pprint
from exchanges.exchangefactory import ExchangeFactory

fac = ExchangeFactory();

a = fac.create('poloniex');
exchange_sets = {};

exchange_sets["poloniex"] = a.getLongShortPairs();
for key in exchange_sets:
    for key_b in exchange_sets[key]:
        print key_b
        print exchange_sets[key][key_b];
