import json
import datetime
import time
from Parser import Parser


class FileWriter:

    @staticmethod
    def store_stats(stats_json, trade_string):
        
        mainCoin = Parser.separateTradeString(trade_string)['first']
        #Writing to file.
        with open('data/' + mainCoin + '_history/' + trade_string + '.json', 'w+') as json_file:
            json.dump(stats_json, json_file)
            json_file.close()

        print("Updated " + trade_string + ".json")

    @staticmethod
    def record_trans(trade_string, is_buying, coin1amount, coin2amount, exchangePrice):
        trans_data = None
        string_data = Parser.separateTradeString(trade_string)
        first_coin = string_data['first']
        second_coin = string_data['second']
        try:
            with open('data/' + first_coin + '_history/' + trade_string + '.json') as json_file:
                trans_data = json.load(json_file)
                json_file.close()
        except:
            print("Transaction data for " + trade_string + " does not exist yet. Creating...")

        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')
        with open('data/' + first_coin + '_history/' + trade_string + '.json', 'w') as json_file:
            if trans_data is None:
                json.dump({"data": [{"date": st, "isPurchase": is_buying, "lost": coin1amount, "gain": coin2amount,
                                     "exchangePrice": exchangePrice}]},
                          json_file)
                json_file.close()
            else:
                json.dump({"data": trans_data['data'] + [
                    {"date": st, "isPurchase": is_buying, "lost": coin1amount, "gain": coin2amount,
                     "exchangePrice": exchangePrice}]},
                          json_file)
                json_file.close()

        print(st)
        print("Stored crypto_data")
