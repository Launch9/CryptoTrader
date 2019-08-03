from FileReader import FileReader
from StatsGiver import StatsGiver
from GF import GF
from Parser import Parser
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
        #GF.pretty_print(market)
        for i in market:
            GF.pretty_print(StatsGiver.get_average_trade_extra(Parser.reverse_trade_string(i['MarketName']), "DAY_1"))


    def update(self):
        for node in self.nodes:
            node.update()
