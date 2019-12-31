# importing the requests library
import requests
import HeavyAl
import time
import timeit
import json

from Parser import Parser
from FileReader import FileReader
from GF import GF


class StatsGiver:

   
    @staticmethod
    def get_stats():

        # api-endpoint
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

        params = {
            'start': '1',
            'limit': '5',
            'convert': 'USD'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'eb53bc71-efbc-4363-b2d1-47bd95eb5578',
        }
        # sending get request and saving the response as response object
        r = requests.get(url=url, params=params, headers=headers, verify=True)

        if (r.ok == False):
            return False
        else:
            return r.json()['result']

    @staticmethod
    def convert_usd_to_crypto(currency, how_much_usd):
        # api-endpoint
        url = "https://api.cryptonator.com/api/ticker/usd-" + currency

        headers = {
            'Accepts': 'application/json',
        }

        # sending get request and saving the response as response object
        r = requests.get(url=url, headers=headers, verify=True).json()
        
        if (r['success'] == False):
            return False
        else:
            return (float(r['ticker']['price']) * how_much_usd);

    @staticmethod
    def convert_crypto_to_usd(currency, how_much_crypto):
         # api-endpoint
        url = "https://api.cryptonator.com/api/ticker/" + currency + "-usd"

        headers = {
            'Accepts': 'application/json',
        }

        # sending get request and saving the response as response object
        r = requests.get(url=url, headers=headers, verify=True).json()
       
        
        if (r['success'] == False):
            return False
        else:
            return (float(r['ticker']['price']) * how_much_crypto)
    @staticmethod
    def get_market():
        # api-endpoint
        url = "https://api.bittrex.com/api/v1.1/public/getmarkets"

        headers = {
            'Accepts': 'application/json',
        }
        # sending get request and saving the response as response object
        r = requests.get(url=url, headers=headers, verify=True)

        if (r.ok == False):
            return False
        else:
            return r.json()['result']

    @staticmethod
    def get_market_summaries():
        # api-endpoint
        url = "https://api.bittrex.com/api/v1.1/public/getmarketsummaries"

        headers = {
            'Accepts': 'application/json',
        }
        # sending get request and saving the response as response object
        r = requests.get(url=url, headers=headers, verify=True)

        if (r.ok == False):
            return False
        else:
            return r.json()['result']

    @staticmethod
    def get_market_summary(tradeString):
        # api-endpoint
        url = "https://api.bittrex.com/api/v1.1/public/getmarketsummary?market=" + tradeString

        headers = {
            'Accepts': 'application/json',
        }
        # sending get request and saving the response as response object
        r = requests.get(url=url, headers=headers, verify=True)

        if (r.ok == False):
            return False
        else:
            return r.json()['result']

    @staticmethod  # Gets the average trade price for the trade. !!! Does not work well with altcoins !!!
    def get_average_trade(trade_string, interval):
        candles = StatsGiver.get_market_candles(trade_string, interval)
        if candles != False:
            stat_sum = 0
            for i in candles:
                stat_sum += ((float(i['O']) + float(i['C'])) / 2)
            return stat_sum / len(candles)
        else:
            return False

    @staticmethod  # Gets the average trade price for the trade. !!! Does not work well with altcoins !!!
    def get_average_trade_extra(trade_string, interval, algo_num):
        if(GF.CONFIG['MODE'] == 0):
            candles = StatsGiver.get_market_candles(trade_string, interval)
        elif(GF.CONFIG['MODE'] == 1):
            candles = StatsGiver.get_saved_market_candles(trade_string, interval)
        if(candles == False):
            return -1
        if(candles['success'] == False):
            return False
        #candles = candles[(len(candles) - 30):]
        if candles != False:
            switcher = {
               0: HeavyAl.algo1
            }
            
            time1 = time.time()
            #Get the function from switcher dictionary
            func = switcher.get(0, lambda a, b, c: None)
            answer = func(trade_string, interval, candles['result'])
            
            return {'data':candles, 'answer':answer}
            
            # return func()
        else:
            return False

   # def get_old_market_candles(trade_string, interval):


    @staticmethod  # Get the the history of the market
    def get_market_candles(trade_string, interval):

        # api-endpoint
        url = "https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=" + Parser.reverse_trade_string(trade_string) + "&tickInterval=onemin&_=1499127220008"
        #url = "https://api.bittrex.com/v3/markets/" + trade_string + "/candles?candleInterval=" + interval

        headers = {
            'Accepts': 'application/json',
        }
        # sending get request and saving the response as response object
        r = requests.get(url=url, headers=headers, verify=True)

        if (r.ok == False):
            return False
        else:
            return r.json()

    @staticmethod
    def get_saved_market_candles(trade_string, interval):
        return FileReader.read_history(trade_string)['result']
