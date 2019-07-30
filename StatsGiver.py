# importing the requests library
import requests
import json


class StatsGiver:
    x = 4

    def __init__(self):
        print("Initializing object!")

    def get_stats(self):

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

        # extracting data in json format
        data = r.json();

        print(json.dumps(data, indent=4, sort_keys=True))

        return data

    def get_market(self):
        # api-endpoint
        url = "https://api.bittrex.com/api/v1.1/public/getmarkets"


        headers = {
            'Accepts': 'application/json',
        }
        # sending get request and saving the response as response object
        r = requests.get(url=url, headers=headers, verify=True)

        # extracting data in json format
        data = r.json()

        #print(json.dumps(data, indent=4, sort_keys=True))

        return data['result']

    def get_market_summaries(self):
        # api-endpoint
        url = "https://api.bittrex.com/api/v1.1/public/getmarketsummaries"


        headers = {
            'Accepts': 'application/json',
        }
        # sending get request and saving the response as response object
        r = requests.get(url=url, headers=headers, verify=True)

        # extracting data in json format
        data = r.json()

        #print(json.dumps(data, indent=4, sort_keys=True))

        return data['result']

    def get_market_summary(self, tradeString):
        # api-endpoint
        url = "https://api.bittrex.com/api/v1.1/public/getmarketsummary?market=btc-ltc"

        headers = {
            'Accepts': 'application/json',
        }
        # sending get request and saving the response as response object
        r = requests.get(url=url, headers=headers, verify=True)

        # extracting data in json format
        data = r.json()

        # print(json.dumps(data, indent=4, sort_keys=True))

        return data['result']