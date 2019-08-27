from FileReader import FileReader
from StatsGiver import StatsGiver
from FileWriter import FileWriter
from GF import GF
import time
import datetime
from Node import Node
from Parser import Parser
import timeit
import PInfo
class Factory:
    MINIMUM_INVEST_PERCENT = 40.0
    MINIMUM_INVEST_USD = 10 #Ten dollars
    nodes = []
    mainCoin = ""
    name = ""
    maxNodes = 10

    def __init__(self, factory_name, main_coin, max_nodes):
        self.name = factory_name
        self.mainCoin = main_coin
        self.maxNodes = max_nodes
        self.create_nodes()

    def create_nodes(self):
        wallet = PInfo.get_wallet()
        market = Parser.find_market_strings(self.mainCoin, StatsGiver.get_market_summaries())
        usd = StatsGiver.convert_crypto_to_usd(self.mainCoin, next((x for x in wallet["result"] if x["Currency"] == self.mainCoin), None)["Available"])
        print("THIS IS THE USD EQUIV")
        print(usd)
        print("THIS IS THE END OF USD EQUIV")
        investment_data = []
        
        for i in market:
            is_ok = False
            while(is_ok == False):
                data = StatsGiver.get_average_trade_extra(Parser.reverse_trade_string(i['MarketName']), "DAY_1", 1)
                if data != False:
                    GF.pretty_print(data)
                    is_ok = True
                    investment_data.append(data)
                    time.sleep(1.1)
                else:
                    is_ok = False
                    print("Failed to get data")
                    time.sleep(15)

        top_investments = []
        # Now that I have all the data I need, I am going to loop through and pick out the best investments.
        print("RESULTS I WANTED=-=-=-=-=-=-=-=-=-=")
        top_investments = investment_data
        top_investments.sort(key=lambda x: x['percent'])
        for i in reversed(top_investments):
            if(i['currentPos'] == -2 and float(i['percent']) > self.MINIMUM_INVEST_PERCENT):
                print("Node created!")
                GF.pretty_print(i);
                #Getting current time stamp.
                st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')
                #Stamping the object
                i['timeStamp'] = str(st)
                #Getting the history file related to the market we are using.
                history = FileReader.read_history(i['marketName'])
                #Adding/updating data to history file
                history['candles'] = StatsGiver.get_market_candles(i["marketName"], "DAY_1")
                history['data'].append(i)
                
                FileWriter.store_stats(history, Parser.reverse_trade_string(i['marketName']))

                self.__create_node(Parser.reverse_trade_string(i['marketName']), StatsGiver.convert_usd_to_crypto(self.mainCoin,self.MINIMUM_INVEST_USD));
                    
    def __create_node(self, trade_string, how_much):
        self.nodes.append(Node(trade_string,how_much))

    def update(self):
        for node in self.nodes:
            node.update()
