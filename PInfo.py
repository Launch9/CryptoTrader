import hmac
import hashlib
import base64
import requests
import json
import time
from GF import GF

API_SECRET_KEY = b''
API_KEY = ''

def signed_request(url):
    now = time.time()
    url += '&nonce=' + str(now)
    signed = hmac.new(API_SECRET_KEY, url.encode('utf-8'), hashlib.sha512).hexdigest()
    headers = {'Accepts': 'application/json', 'apisign': signed}
    r = requests.get(url, headers=headers, verify=True)
    return r.json()

def get_wallet():
    r = signed_request('https://api.bittrex.com/api/v1.1/account/getbalances?apikey=fdc2041e393c4f43a96f4a24f48a9374')

    print(r)
    if (r['success'] == False):
        return False
    else:
        return r.json()

def get_currency(currency):
    r = signed_request('https://api.bittrex.com/api/v1.1/account/getbalance?apikey=fdc2041e393c4f43a96f4a24f48a9374&currency=BTC')

    print(r)
    if (r['success'] == False):
        return False
    else:
        return r.json()