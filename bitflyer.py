#!/usr/bin/env python3
""" Get JSON data from bitflyer"""

import sys
import pprint
import requests

ENDPOINT="https://api.bitflyer.com/v1/"

def get_data(query, print_query=False):
    """ get_data() """
    full_query = ENDPOINT + query

    if print_query:
        print(f"Query: {full_query}")
    req = requests.get(full_query)
    
    if req.status_code != 200:
        print(f"{req.status_code}.")
        print(full_query)
        sys.exit(1)
    
    if not req.json():
        print("No data returned with the following query.")
        print(full_query)
        sys.exit(0)
        
    return req


def get_markets():
    """ get_markets() """
    dicts_list =  get_data("getmarkets").json()
    return dicts_list

def get_board(product_code):
    """ get_board() """
    req = get_data("board" + '?' + product_code, True)
    data = req.json()
    return data

def get_ticker(product_code):
    """ get_ticker() """
    req = get_data("ticker" + '?' + product_code, True)
    data = req.json()
    return data

def my_market_condition(data):
    """ my_market_condition() """
    rcode = True
    if data['market_type'] == 'Futures':
        rcode = False
    elif data['product_code'] in ("BTC_JPY", "FX_BTC_JPY") :
        pass
    return rcode

def main4():
    """ main() """
    markets = [d for d in get_markets() if my_market_condition(d)]

    for market in markets:
        data = get_board(market["product_code"])
        print(data["mid_price"])
        data2 = get_ticker(market["product_code"])
        pprint.pprint(data2)


if __name__ == '__main__':
    main4()
