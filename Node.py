from StatsGiver import StatsGiver
from Parser import Parser
import time
import datetime
from GF import GF
from FileReader import FileReader
from FileWriter import FileWriter

class Node:
    tradeString = None
    initMCValue = None #Initial main factory coin value since creation
    initUSD = None
    data = None
    mainCoin = None
    def __init__(self, trade_string, how_much, data, mainCoin):
        self.tradeString = trade_string
        self.initMCValue = how_much
        self.initUSD = StatsGiver.convert_crypto_to_usd(Parser.separateTradeString(trade_string)["first"], how_much)
        self.data = data
        self.mainCoin = mainCoin
        self.__update_history()
        print("NODE CREATED WITH DATA:")
        GF.pretty_print(data)
        
    def __update_history(self):
        #Getting current time stamp.
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')
        #Stamping the object
        self.data['timeStamp'] = str(st)
        #Getting the history file related to the market we are using.
        history = FileReader.read_history(self.data['marketName'])
        #Adding/updating data to history file
        history['result'] = StatsGiver.get_market_candles(self.data["marketName"], "DAY_1")
        history['data'].append(self.data)
        
        FileWriter.store_stats(history, Parser.reverse_trade_string(self.data['marketName']))
        time.sleep(1.1) 

    def update(self):
        print("GETTING MARKET SUMMARY")
        summary = StatsGiver.get_market_summary(self.tradeString)
        GF.pretty_print(summary)
        