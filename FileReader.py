from ConfigData import ConfigData
import json
from Parser import Parser
from os import listdir
from os.path import isfile, join
from GF import GF
class FileReader:

    @staticmethod
    def get_all_trade_data():
        re = []
        mypath = "./data/ETH_history"
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for i in onlyfiles:
            data = FileReader.read_data("data/ETH_history/" + i)['data'][0]
            GF.pretty_print(data)
            re.append(data)

        mypath = "./data/BTC_history"
        onlyfiles = ([f for f in listdir(mypath) if isfile(join(mypath, f))])
        for i in onlyfiles:
            data = FileReader.read_data("data/BTC_history/" + i)['data'][0]
            GF.pretty_print(data)
            re.append(data)

        mypath = "./data/USDT_history"
        onlyfiles = ([f for f in listdir(mypath) if isfile(join(mypath, f))])
        for i in onlyfiles:
            data = FileReader.read_data("data/USDT_history/" + i)['data'][0]
            GF.pretty_print(data)
            re.append(data)

        return re

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
    def read_data(filePath):
        try:
            with open(filePath) as json_file:
                return json.load(json_file)
        except:
            return {"data":[]}

    @staticmethod
    def read_history(tradeString):
        mainCoin = Parser.separateTradeString(tradeString)['first']
        try:
            with open("data/" + mainCoin + "_history/" + tradeString + ".json") as json_file:
                return json.load(json_file)
        except:
            return {"candles":{}, "data":[]}

