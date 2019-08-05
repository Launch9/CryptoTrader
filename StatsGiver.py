# importing the requests library
import requests
import HeavyAl
import json
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
                stat_sum += ((float(i['open']) + float(i['close'])) / 2)
            return stat_sum / len(candles)
        else:
            return False

    @staticmethod  # Gets the average trade price for the trade. !!! Does not work well with altcoins !!!
    def get_average_trade_extra(trade_string, interval, algo_num):
        candles = StatsGiver.get_market_candles(trade_string, interval)
        if candles != False:
            switcher = {
               0: HeavyAl.algo1,
            }
            #Get the function from switcher dictionary
            func = switcher.get(0, lambda a, b, c: None)
            return func(trade_string, interval, candles)
            # return func()
        else:
            return False

    @staticmethod  # Get the the history of the market
    def get_market_candles(trade_string, interval):

        # api-endpoint
        url = "https://api.bittrex.com/v3/markets/" + trade_string + "/candles?candleInterval=" + interval

        headers = {
            'Accepts': 'application/json',
        }
        # sending get request and saving the response as response object
        r = requests.get(url=url, headers=headers, verify=True)

        if (r.ok == False):
            return False
        else:
            return r.json()
