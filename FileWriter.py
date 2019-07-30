import json
import datetime
import time
from Parser import Parser


class FileWriter:
    parser = Parser()

    def __init__(self):
        print("Initialzing FileWriter!")

    def store_stats(self, stats_json):
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')
        with open('BTC_history/crypto_data_' + str(st) + '.json', 'w') as json_file:
            json.dump(stats_json, json_file)
            json_file.close()

        print(st)
        print("Stored crypto_data")

    def record_trans(self, trade_string, is_buying, coin1amount, coin2amount, exchangePrice):
        trans_data = None

        try:
            with open('data/BTC_history/' + trade_string + '.json') as json_file:
                trans_data = json.load(json_file)
                json_file.close()
        except:
            print("Transaction data for " + trade_string + " does not exist yet. Creating...")


        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')
        with open('data/BTC_history/' + trade_string + '.json', 'w') as json_file:
            if trans_data is None:
                json.dump({"data": [{"date": st, "isPurchase": is_buying, "lost": coin1amount, "gain": coin2amount, "exchangePrice":exchangePrice}]},
                          json_file)
                json_file.close()
            else:
                json.dump({"data": trans_data['data'] + [{"date": st, "isPurchase": is_buying, "lost": coin1amount, "gain": coin2amount,
                                     "exchangePrice": exchangePrice}]},
                          json_file)
                json_file.close()

        print(st)
        print("Stored crypto_data")
