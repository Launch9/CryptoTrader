from StatsGiver import StatsGiver
from Parser import Parser
import time
import datetime
from FileReader import FileReader
from FileWriter import FileWriter

class Node:
    tradeString = None
    initMCValue = None #Initial main factory coin value since creation
    initUSD = None
    data = None
    def __init__(self, trade_string, how_much, data):
        self.tradeString = trade_string
        self.initMCValue = how_much
        self.initUSD = StatsGiver.convert_crypto_to_usd(Parser.separateTradeString(trade_string)["first"], how_much)
        self.data = data
        self.__update_history()
        
    def __update_history(self):
        #Getting current time stamp.
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')
        #Stamping the object
        self.data['timeStamp'] = str(st)
        #Getting the history file related to the market we are using.
        history = FileReader.read_history(self.data['marketName'])
        #Adding/updating data to history file
        history['candles'] = StatsGiver.get_market_candles(self.data["marketName"], "DAY_1")
        history['data'].append(self.data)
        
        FileWriter.store_stats(history, Parser.reverse_trade_string(self.data['marketName']))

    def update(self):
        print("Updating node!")
