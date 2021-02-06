#!/usr/bin/env python3

import requests
import sys
import pprint

ENDPOINT="https://api.bitflyer.com/v1/"

def get_data(query, print_query=False):
    full_query = ENDPOINT + query
    
    if print_query:
        print(f"Query: {full_query}")
    r = requests.get(full_query)
    
    if r.status_code != 200:
        print(f"{r.status_code}.")
        print(full_query)
        sys.exit(1)
    
    if not r.json():
        print("No data returned with the following query.")
        print(full_query)
        sys.exit(0)
    
    return r


def get_markets():
    dicts_list =  get_data("getmarkets").json()
    return dicts_list

def get_board(product_code):
    r = get_data("board" + '?' + product_code, True)
    dict = r.json()
    return dict

def get_ticker(product_code):
    r = get_data("ticker" + '?' + product_code, True)
    dict = r.json()
    return dict

def my_market_condition(dict):
    if dict['market_type'] == 'Futures':
        return False
    elif dict['product_code'] in ("BTC_JPY", "FX_BTC_JPY") :
        return True
    return False


markets = [d for d in get_markets() if market_condition(d)]

for market in markets:
    d = get_board(market["product_code"])
    print(d["mid_price"])
    d = get_ticker(market["product_code"])
    pprint.pprint(d)
