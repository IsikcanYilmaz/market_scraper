#!/usr/bin/env python3

'''
D E P R I C A T E D
'''

import sys, os, json, fnmatch, codecs

JSON_DIRNAME = "jsons"

def readJsonFile(filename):
    f = open(filename, "r")
    data = json.load(f)
    f.close()
    return data

def getDateFromJsonFile(filename):
    return filename.replace(".json", "").split("_")[-1]

def getMarketFromJsonFIle(filename):
    return filename.split("_")[0]

if JSON_DIRNAME not in os.listdir():
    os.mkdir(JSON_DIRNAME)

filelist = os.listdir()
os.chdir(JSON_DIRNAME)

for filename in filelist:
    newProducts = {}
    if fnmatch.fnmatch(filename, f'*.json'):
        date = getDateFromJsonFile(filename)
        market = getMarketFromJsonFIle(filename)
        print("FILE",filename, date)
        currProducts = readJsonFile(f'../{filename}')
        for category in currProducts:
            print("CATEGORY", category)
            for product in currProducts[category]:
                newProduct = currProducts[category][product]
                newProduct['market'] = market
                newProduct['date'] = date
                newProduct['category'] = category
                newProducts[product] = newProduct
                print("->", product, newProduct)
        with codecs.open(filename, "w", encoding="utf-8") as fp:
            json.dump(newProducts, fp, ensure_ascii=False)
        os.remove(f'../{filename}')

os.chdir("..")
