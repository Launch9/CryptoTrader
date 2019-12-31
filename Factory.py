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
    MINIMUM_PROFIT_NOPS = 5
    
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
        #usd = StatsGiver.convert_crypto_to_usd(self.mainCoin, next((x for x in wallet["result"] if x["Currency"] == self.mainCoin), None)["Available"])
        
        investment_data = []
        
        for i in market:
            is_ok = False
            while(is_ok == False):
                if(Parser.is_valid_trade(i['MarketName'])):
                    data = StatsGiver.get_average_trade_extra(Parser.reverse_trade_string(i['MarketName']), "DAY_1", 1)
                    if data != False and data != -1:
                        GF.pretty_print(data['answer'])
                        is_ok = True
                        investment_data.append(data['answer'])
                        FileWriter.store_stats(data['data']['result'], i['MarketName'])
                        if(GF.CONFIG["MODE"] == 0):
                            time.sleep(2.0)
                        
                        
                    elif data == -1:
                        is_ok = False
                        print("Failed to get data")
                        if(GF.CONFIG["MODE"] == 0):
                            time.sleep(15)
                    else:
                        is_ok = True
                        print("NOT A VALID MARKET")
                        time.sleep(2.0)
                        
                else:
                    is_ok = True
                
        
        #investment_data = FileReader.get_all_trade_data()
        top_investments = []
        # Now that I have all the data I need, I am going to loop through and pick out the best investments.
        print("RESULTS I WANTED=-=-=-=-=-=-=-=-=-=")
        top_investments = investment_data
       
        # Sorting an finding what stats have value.
        top_investments.sort(key=lambda x: int(x['nop-profit']))
        profit_nop_range = (float(top_investments[len(top_investments) - 1]['nop-profit']) - float(top_investments[0]['nop-profit']))
        profit_nop_value = 100 / profit_nop_range
        
        top_investments.sort(key=lambda x: float(x['cpi']))
        percent_range = (float(top_investments[len(top_investments) - 1]['cpi']) - float(top_investments[0]['cpi']))
        percent_value = 100 / percent_range

        """top_investments.sort(key=lambda x: int(x['candleLength']))
        candle_range = (float(top_investments[len(top_investments) - 1]['candleLength']) - float(top_investments[0]['candleLength']))
        candle_value = 100 / candle_range"""
        
        top_investments2 = []
        for i in top_investments:
            invest_value = (float(i['nop-profit']) * profit_nop_value) + (float(i['cpi']) * percent_value)
            i['investValue'] = invest_value
            top_investments2.append(i)
            
            
        top_investments2.sort(key=lambda x: x['investValue'])
        #top_investments2.sort(key=lambda x: x['nop-profit'])
        for i in top_investments2: 
            GF.pretty_print(i)
            """if(GF.CONFIG["MODE"] == 0):
                print("Node created!")
                #Getting current time stamp.
                st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')
                #Stamping the object
                i['timeStamp'] = str(st)
                #Getting the history file related to the market we are using.
                history = FileReader.read_history(i['marketName'])
                #Adding/updating data to history file
                history['result'] = StatsGiver.get_market_candles(i["marketName"], "DAY_1")
                time.sleep(1.1)
                history['data'].append(i)
               
                #FileWriter.store_stats(history, i['marketName'])
                if(i['currentPos'] == -2 and float(i['cpi']) < 100):
                    self.__create_node(Parser.reverse_trade_string(i['marketName']), StatsGiver.convert_usd_to_crypto(self.mainCoin,self.MINIMUM_INVEST_USD), i)
            else:
                GF.pretty_print(i)"""
            
                
                    
    def __create_node(self, trade_string, how_much, data):
        b = 5
        #self.nodes.append(Node(trade_string,how_much, data, self.mainCoin))

    def update(self):
        for node in self.nodes:
            node.update()
