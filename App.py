
import json
#import timeit
import subprocess
subprocess.call(["cython", "-a", "HeavyAl.pyx"])
print('Compiled cython modules!')
from Factory import Factory
import time
from FileReader import FileReader
import PInfo
from GF import GF
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
        config_data = FileReader.read_config()
        GF.CONFIG = config_data

    def create_factories(self):
        usdtf1 = Factory("usdtf1", "USDT", 2)
        ethf2 = Factory("ethf1", "ETH", 2)
        btcf3 = Factory("btcf1", "USDT", 2)
        btcf = Factory("btchf1", "USD", 2)
        self.factories.append(usdtf1)
        #self.factories.append(ethf2)
        #self.factories.append(btcf3)

    def update_factories(self):
        for factory in self.factories:
            factory.update()

    def run(self):
        print("Running...")

        self.create_factories()
        #print(PInfo.get_wallet())
        #GF.pretty_print(StatsGiver.get_average_trade_extra("LTC-BTC", "DAY_1"))
        while self.isRunning:

            # Reading config file for updates from node.js server

            config_data = FileReader.read_config()
            GF.CONFIG = config_data
            # Checking to see if server should continue to run
            self.isRunning = config_data["IS_ACTIVE"]

            self.update_factories()

            # Sleeping thread to wait for market to change
            time.sleep(60 * config_data["SLEEP_TIME_MINUTES"])

        print("Shutting down!")
        time.sleep(3)
