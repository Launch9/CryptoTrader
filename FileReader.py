from ConfigData import ConfigData
import json
from Parser import Parser

class FileReader:

    @staticmethod
    def read_config():
        with open('data/config.json') as json_file:
            return json.load(json_file)

    @staticmethod
    def get_wallet():
        with open('data/wallet.json') as json_file:
            return json.load(json_file)

    @staticmethod
    def update_wallet(data):
        with open('data/wallet.json', 'w') as json_file:
            json.dump(data, json_file)
            json_file.close()

    @staticmethod
    def read_history(tradeString):
        mainCoin = Parser.separateTradeString(tradeString)['first']
        try:
            with open("data/" + mainCoin + "_history/" + tradeString) as json_file:
                return json.load(json_file)
        except:
            return {"candles":{}, "data":[]}

