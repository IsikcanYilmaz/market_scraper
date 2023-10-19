#!/usr/bin/env python3

import sqlite3
import fnmatch
import json
import sys, os
from datetime import datetime

JSON_DIR = "/home/jon/KODMOD/market_scraper/jsons"
DATABASE_NAME = "products.db"

CREATE_TABLE_SQL = '''
CREATE TABLE products (
	name TEXT not null,
	oldPrice INTEGER,
	currentPrice INTEGER not null,
	market TEXT not null,
	date TEXT not null,
    timestamp INTEGER not null,
	category TEXT not null
);
'''

def convertDateStrToTimestamp(dateStr):
    # Date str: DD-MM-YYYY
    dateArr = dateStr.split("-")
    year = int(dateArr[2])
    month = int(dateArr[1])
    day = int(dateArr[0])
    dt = datetime(
            year = year,
            month = month,
            day = day
            )
    return int(dt.timestamp())

def readJsonFile(filename):
    f = open(filename, "r")
    data = json.load(f)
    f.close()
    return data

def insertNewProduct(productName, productDict, cursor):
    timestamp = convertDateStrToTimestamp(productDict['date'])
    sqlStr = (f'INSERT INTO products (name, oldPrice, currentPrice, market, date, timestamp, category) VALUES ("{productName}", "{productDict["oldPrice"]}", "{productDict["currentPrice"]}", "{productDict["market"]}", "{productDict["date"]}", "{timestamp}", "{productDict["category"]}")')
    print(sqlStr)
    cursor.execute(sqlStr)

def populateDb(filename, cursor):
    date = filename.replace(".json", "").split("_")[-1]
    market = filename.split("_")[0]
    jsonData = readJsonFile(filename)
    for productName in jsonData:
        productDict = jsonData[productName]
        insertNewProduct(productName, productDict, cursor)
        # print(productName)

def main():
    # Create database
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    try:
        cursor.execute(CREATE_TABLE_SQL)
    except sqlite3.OperationalError:
        print("[*] Table already exists")

    # Parse json files
    os.chdir(JSON_DIR)
    ls = os.listdir()
    for filename in ls:
        if fnmatch.fnmatch(filename, f'*.json'):
            print(filename)
            populateDb(filename, cursor)
    connection.commit()

if __name__ == "__main__":
    main()
