#!/usr/bin/env python3 

import sys, os, fnmatch
import json
import sqlite3
from datetime import datetime

MARKETS = ["a101"]

def createDatabase():
    pass

def loadDatabase():
    pass

def main():
    # Check if database exists. Create one if not
    # TODO

    # Go thru our json files. Record them in our database
    products = {}
    for m in MARKETS:
        filenames = []
        for filename in os.listdir("."):
            print(getDateFromJsonFile(filename))
            return
            if fnmatch.fnmatch(filename, f'{m}_*.json'):
                date = getDateFromJsonFile(filename)
                filenames.append(filename)
                currProducts = readJsonFile(filename)
                for category in currProducts:
                    # FOR NOW LETS NOT CATEGORIZE
                    # if category not in products:
                    #     products.append({category:[]})
                    # if p in products:
                    #     print(f'{p} exists!')
                    # else:
                    #     print(f'{p} added!')
                    print("CATEGORY", category)
                    for product in currProducts[category]:
                        print(product)
                print(f'[*] Found: {filename}. {m}, date: {date}')

def getDateFromJsonFile(filename):
    return filename.replace(".json", "").split("_")[-1]

def readJsonFile(filename):
    f = open(filename, "r")
    data = json.load(f)
    f.close()
    return data

if __name__ == "__main__":
    main()
