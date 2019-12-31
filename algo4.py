#!/usr/bin/python
# /examples/order_book.py

# Sample script showing how order book syncing works.

from __future__ import print_function
from time import sleep
from bittrex_websocket import OrderBook
import json
from GF import GF
def getOrderData(data):
    buySize = len(data['Z'])
    sellSize = len(data['S'])
    buyVolume = 0
    sellVolume = 0
    for i in data['Z']:
        buyVolume += i['R']
    for i in data['S']:
        sellVolume += i['R']
    return {"data":{"size": {"buy": buySize, "sell": sellSize}, "volume":{"buy":buyVolume, "sell":sellVolume}}}
def main():
    class MySocket(OrderBook):
        def on_ping(self, msg):
            
            #print('Received order book update for {}'.format(msg))
            print(msg)

    # Create the socket instance
    ws = MySocket()
    # Enable logging
    ws.enable_log()
    # Define tickers
    tickers = ['USDT-ETH']
    # Subscribe to order book updates
    ws.subscribe_to_orderbook(tickers)

    while True:
        sleep(10)
        book = ws.get_order_book('USDT-ETH')
        #GF.pretty_print(getOrderData(book))
        """with open("./orderBook.json", 'w') as json_file:
            json.dump(book, json_file)
            json_file.close()"""
    else:
        pass

if __name__ == "__main__":
    main()