#!/usr/bin/env python3

import sys, os
import codecs
import argparse
import requests
import traceback
import json
import time
from datetime import datetime
from bs4 import BeautifulSoup

URLS = {'a101'  : {'base':'https://www.a101.com.tr/market',
                  'subs':['temel-gida', 'atistirmalik', 'ev-bakim-temizlik', 'icecek', 'ambalaj-malzemeleri', 'kahvaltilik-sut-urunleri', 'saglikli-yasam-urunleri', 'meyve-sebze']},
        'sok'   : {'base':'https://www.sokmarket.com.tr/',
                  'subs':['meyve-sebze-c-1396', 'et-tavuk-sarkuteri-c-1242', 'sut-ve-sut-urunleri-c-1244', 'kahvaltilik-c-1245', 'ekmek-pastane-c-1249', 'dondurulmus-urunler-c-1914', 'yemeklik-malzemeler-c-1243', 'atistirmalik-c-1885', 'icecek-c-1247', 'kisisel-bakim-kozmetik-c-1250', 'anne-bebek-cocuk-c-1743', 'temizlik-c-1248', 'kagit-urunleri-c-1915', 'evcil-dostlar-c-1947', 'elektronik-c-1251', 'giyim-ayakkabi-aksesuar-c-1893', 'ev-yasam-c-1897']},
        'migros': {'base':'https://www.migros.com.tr/',
                  'subs':['meyve-sebze-c-2', 'et-tavuk-balik-c-3', 'sut-kahvaltilik-c-4', 'temel-gida-c-5', 'meze-hazir-yemek-donuk-c-7d', 'firin-pastane-c-7e', 'dondurma-c-41b', 'atistirmalik-c-113fb', 'icecek-c-6', 'deterjan-temizlik-c-7', 'kagit-islak-mendil-c-8d', 'kisisel-bakim-kozmetik-saglik-c-8', 'bebek-c-9', 'ev-yasam-c-a', 'kitap-kirtasiye-oyuncak-c-118ec', 'cicek-c-502', 'pet-shop-c-a0', 'elektronik-c-a6']}
        }

CURRENCIES = {'tl':'₺'}

POLITE = True
POLITE_SLEEP = 1 # second

class Migros_Scraper():
    def __init__(self):
        self.name = "migros"
        self.baseUrl = URLS[self.name]['base']
        self.subs = URLS[self.name]['subs']
        self.currency = 'tl'
        self.currencyChar = CURRENCIES[self.currency]
        self.products = {}

    def operate(self):
        print("[*] Scraping Migros")
        for sub in self.subs:
            print(f'[*] Scraping "{sub}"')
        initPageUrl = f'{self.baseUrl}/{sub}'
        print(">", initPageUrl)
        initPageHtml = requests.get(initPageUrl)
        soup = BeautifulSoup(initPageHtml.content, "html.parser")
        # numPages = 


    def parse(self):
        pass

class Sok_Scraper():
    def __init__(self):
        self.name = "sok"
        self.baseUrl = URLS[self.name]['base']
        self.subs = URLS[self.name]['subs']
        self.currency = 'tl'
        self.currencyChar = CURRENCIES[self.currency]
        self.products = {}

    def operate(self):
        print("[*] Scraping SOK")
        for sub in self.subs:
            print(f'[*] Scrapging "{sub}"')
            initPageUrl = f'{self.baseUrl}/{sub}'
            print("> ", initPageUrl)
            initPageHtml = requests.get(initPageUrl)
            soup = BeautifulSoup(initPageHtml.content, 'html.parser')
            numPages = len(soup.find_all(class_="js-pagination"))
            # products = {}
            # products.update(self.parse(soup))
            print(soup)
            # print(products)

    def parse(self, soup):
        return soup

class A101_Scraper():
    def __init__(self):
        self.name = 'a101'
        self.baseUrl = URLS[self.name]['base']
        self.subs = URLS[self.name]['subs']
        self.currency = 'tl'
        self.currencyChar = CURRENCIES[self.currency]
        self.products = {}

    def operate(self):
        print("[*] Scraping A101")
        for sub in self.subs:
            print(f'[*] Scraping "{sub}"')
            if not sub in self.products:
                self.products[sub] = {}
            initPageUrl = f'{self.baseUrl}/{sub}'
            print("> ", initPageUrl)
            initPageHtml = requests.get(initPageUrl)
            soup = BeautifulSoup(initPageHtml.content, 'html.parser')
            numPages = len(soup.find_all(class_="js-pagination"))
            products = {}
            products.update(self.parse(soup))
            if (numPages > 1):
                for p in range(2, numPages+1):
                    if (POLITE):
                        time.sleep(POLITE_SLEEP)
                    url = f'{initPageUrl}/?page={p}'
                    print("> ", url)
                    html = requests.get(url)
                    soup = BeautifulSoup(html.content, "html.parser")
                    products.update(self.parse(soup))
            self.products[sub] = products
        jsonFilename = f'a101_{datetime.today().strftime("%d-%m-%Y")}.json'
        with codecs.open(jsonFilename, "w", encoding='utf-8') as fp:
            json.dump(self.products, fp, ensure_ascii=False)
        print(f'[*] Written to {jsonFilename}')

    def parse(self, soup):
        # Get all products' name, price, old price (if exists), picture URL info
        # return in an array of dicts
        productsRaw = soup.find_all(class_="set-product-item")
        products = {}
        for p in productsRaw:
            # get raw texts, split em
            name = p.find(class_="name").text.replace("  ", "").replace("\n", "")
            currentPriceSoup = p.find(class_="current")
            oldPriceSoup = p.find(class_="old")
            imageSoup = p.find("figure").find("img")

            # parse prices
            if (currentPriceSoup is None):
                print(p)
                print(f'[!] No current price for {name}! Skipping')
                continue
            currentPrice = float(currentPriceSoup.text.replace(self.currencyChar, "").replace(",", "."))
            
            oldPrice = None
            if (oldPriceSoup is not None):
                oldPrice = float(oldPriceSoup.text.replace(self.currencyChar, "").replace(",", "."))

            # productDict = {name:{'oldPrice':oldPrice, 'currentPrice':currentPrice, 'imageUrl':imageSoup['data-src']}}
            try:
                imageSoup['data-src']
            except KeyError:
                print("[!] data-src field not found for", name)
                imageSoup['data-src'] = None
            products[name] = {'oldPrice':oldPrice, 'currentPrice':currentPrice, 'imageUrl':imageSoup['data-src']} 
            # products.append(productDict)
        return products

def main():
    a101Obj = A101_Scraper()
    sokObj = Sok_Scraper()
    a101Obj.operate()
    # sokObj.operate()

if __name__ == "__main__":
    main()
