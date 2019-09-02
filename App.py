
import json
#import timeit
#import subprocess
#subprocess.call(["cython", "-a", "HeavyAl.pyx"])
print('Compiled cython modules!')
from Factory import Factory
import time
from FileReader import FileReader
import PInfo
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
        ethf1 = Factory("ethf1", "USDT", 2)
        self.factories.append(ethf1)

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

            # Checking to see if server should continue to run
            self.isRunning = config_data["IS_ACTIVE"]

            self.update_factories()

            # Sleeping thread to wait for market to change
            time.sleep(60 * config_data["SLEEP_TIME_MINUTES"])

        print("Shutting down!")
        time.sleep(3)
