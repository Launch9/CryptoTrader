from FileReader import FileReader
from StatsGiver import StatsGiver
from GF import GF
import time
from Parser import Parser
import timeit
class Factory:
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
        wallet = FileReader.get_wallet()
        market = Parser.find_market_strings(self.mainCoin, StatsGiver.get_market_summaries())
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
        for i in top_investments:
            GF.pretty_print(i)
        '''for i in investment_data:
            percent = i.percent
            top_investments.sort()
            for b in top_investments
                if percent > b.percent:'''
                    


    def update(self):
        for node in self.nodes:
            node.update()
