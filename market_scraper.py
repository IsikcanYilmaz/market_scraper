#!/usr/bin/env python3

import sys, os
import codecs
import argparse
import requests
import traceback
import json
import time
from datetime import datetime
# from requests_html import HTMLSession, AsyncHTMLSession # https://stackoverflow.com/questions/26393231/using-python-requests-with-javascript-pages
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup

JSON_DIRNAME = "jsons"

URLS = {'a101'  : {'base':'https://www.a101.com.tr/market',
                  'subs':['temel-gida', 'atistirmalik', 'ev-bakim-temizlik', 'icecek', 'ambalaj-malzemeleri', 'kahvaltilik-sut-urunleri', 'saglikli-yasam-urunleri', 'meyve-sebze']},
        'sok'   : {'base':'https://www.sokmarket.com.tr',
                  'subs':['meyve-sebze-c-1396', 'et-tavuk-sarkuteri-c-1242', 'sut-ve-sut-urunleri-c-1244', 'kahvaltilik-c-1245', 'ekmek-pastane-c-1249', 'dondurulmus-urunler-c-1914', 'yemeklik-malzemeler-c-1243', 'atistirmalik-c-1885', 'icecek-c-1247', 'kisisel-bakim-kozmetik-c-1250', 'anne-bebek-cocuk-c-1743', 'temizlik-c-1248', 'kagit-urunleri-c-1915', 'evcil-dostlar-c-1947', 'elektronik-c-1251', 'giyim-ayakkabi-aksesuar-c-1893', 'ev-yasam-c-1897']},
        'migros': {'base':'https://www.migros.com.tr',
                  'subs':['meyve-sebze-c-2', 'et-tavuk-balik-c-3', 'sut-kahvaltilik-c-4', 'temel-gida-c-5', 'meze-hazir-yemek-donuk-c-7d', 'firin-pastane-c-7e', 'dondurma-c-41b', 'atistirmalik-c-113fb', 'icecek-c-6', 'deterjan-temizlik-c-7', 'kagit-islak-mendil-c-8d', 'kisisel-bakim-kozmetik-saglik-c-8', 'bebek-c-9', 'ev-yasam-c-a', 'kitap-kirtasiye-oyuncak-c-118ec', 'cicek-c-502', 'pet-shop-c-a0', 'elektronik-c-a6']},
        'bim'   : {'base':'', 
                   'subs':''}
        }

REQ_HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

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
        initPageHtml = requests.get(initPageUrl, headers=REQ_HEADER)
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

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options)

    def operate(self):
        # Uses selenium due to site being dynamic
        print("[*] Scraping SOK")
        for sub in self.subs:
            initPageUrl = f'{self.baseUrl}/{sub}'
            self.driver.get(initPageUrl)
            productBoxArr = self.driver.find_elements(By.CLASS_NAME, "productbox-wrap")
            for product in productBoxArr:
                name = product.find_element(By.CLASS_NAME, "content-title").text
                imageUrl = product.find_element(By.CLASS_NAME, "image")
                currentPrice = product.find_element(By.CLASS_NAME, "pricetag").text.split("\n") # Hack. find way to extract discount price / curr price correctly
                oldPrice = None
                # try:
                #     oldPrice = currentPrice.find_element(By.CLASS_NAME, "old").text
                # except:
                #     pass
                if (len(currentPrice) > 1):
                    oldPrice = currentPrice[0]
                currentPrice = currentPrice[-1]
                print(f'{name} : current {currentPrice} old {oldPrice} ')
                # print(currentPrice.split("\n"))

            # [print(j, i.text, "\n") for j, i in enumerate(productBoxArr)]
            # # print(productBoxArr)
            # input()
            break

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
            # if not sub in self.products:
            #     self.products[sub] = {}
            initPageUrl = f'{self.baseUrl}/{sub}'
            print("> ", initPageUrl)
            initPageHtml = requests.get(initPageUrl, headers=REQ_HEADER)
            soup = BeautifulSoup(initPageHtml.content, 'html.parser')
            numPages = len(soup.find_all(class_="js-pagination"))
            products = {}
            products.update(self.parse(soup, sub))
            if (numPages > 1):
                for p in range(2, numPages+1):
                    if (POLITE):
                        time.sleep(POLITE_SLEEP)
                    url = f'{initPageUrl}/?page={p}'
                    print("> ", url)
                    html = requests.get(url)
                    soup = BeautifulSoup(html.content, "html.parser")
                    products.update(self.parse(soup, sub))
            self.products.update(products)
        jsonFilename = f'a101_{datetime.today().strftime("%d-%m-%Y")}.json'
        with codecs.open(f'{JSON_DIRNAME}/{jsonFilename}', "w", encoding='utf-8') as fp:
            json.dump(self.products, fp, ensure_ascii=False)
        print(f'[*] Written to {jsonFilename}')

    def parse(self, soup, sub=None):
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
            
            try:
                currentPrice = float(currentPriceSoup.text.replace(self.currencyChar, "").replace(",", "."))
            except ValueError as e:
                print(f'[!] bad string to convert to float "{currentPriceSoup.text}". Name: {name}. Skipping')
                continue 
            
            oldPrice = None
            if (oldPriceSoup is not None):
                oldPrice = float(oldPriceSoup.text.replace(self.currencyChar, "").replace(",", "."))

            # productDict = {name:{'oldPrice':oldPrice, 'currentPrice':currentPrice, 'imageUrl':imageSoup['data-src']}}
            try:
                imageSoup['data-src']
            except KeyError:
                print("[!] data-src field not found for", name)
                imageSoup['data-src'] = None

            # Get other metadata
            date = datetime.today().strftime("%d-%m-%Y")
            products[name] = {'oldPrice':oldPrice, 'currentPrice':currentPrice, 'imageUrl':imageSoup['data-src'], 'market':self.name, 'date':date, 'category':sub} 
            # products.append(productDict)
        return products

def main():
    a101Obj = A101_Scraper()
    sokObj = Sok_Scraper()
    a101Obj.operate()
    # sokObj.operate()

if __name__ == "__main__":
    main()
