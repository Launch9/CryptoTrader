import time
from StatsGiver import StatsGiver
from GraphMaker import GraphMaker
from FileReader import FileReader
from FileWriter import FileWriter
from Parser import Parser
from Trader import Trader
from GF import GF
import time
'''
When to buy:
    Bot buys when currency is below average line by a certain percent.
    
'''


class App:

    waitTime = 10

    parser = Parser()

    fileReader = FileReader()
    graphMaker = GraphMaker()
    statsGiver = StatsGiver()
    fileWriter = FileWriter()
    trader = Trader(fileReader,fileWriter,statsGiver)
    isRunning = True

    def __init__(self):
        print("Initializing app...")

    def run(self):
        print("Running...")

        while self.isRunning:
            # Reading config file for updates from node.js server

            config_data = self.fileReader.read_config()

            # Checking to see if server should continue to run
            self.isRunning = config_data.isActive

            # Updating trade stats
            self.trader.update()

            self.trader.buy("BTC-LTC", 0.05)

            # Sleeping thread to wait for market to change
            time.sleep(60 * config_data.sleepTimeMinutes)

        print("Shutting down!")
        time.sleep(3)
