import time
from StatsGiver import StatsGiver
from GraphMaker import GraphMaker
from FileReader import FileReader
from FileWriter import FileWriter
from Parser import Parser
from Trader import Trader
from GF import GF
from Factory import Factory
import time
'''
When to buy:
    Bot buys when currency is below average line by a certain percent.
    
'''


class App:

    waitTime = 10
    isRunning = True
    factories = []

    def __init__(self):
        print("Initializing app...")

    def create_factories(self):
        usdf1 = Factory("usdf1", "USD", 10)
        self.factories.append(usdf1)

    def update_factories(self):
        for factory in self.factories:
            factory.update()

    def run(self):
        print("Running...")

        self.create_factories()

        #GF.pretty_print(StatsGiver.get_average_trade_extra("LTC-BTC", "DAY_1"))
        """while self.isRunning:
            # Reading config file for updates from node.js server

            config_data = FileReader.read_config()

            # Checking to see if server should continue to run
            self.isRunning = config_data.isActive

            self.update_factories()

            # Sleeping thread to wait for market to change
            time.sleep(60 * config_data.sleepTimeMinutes)

        print("Shutting down!")
        time.sleep(3)"""
