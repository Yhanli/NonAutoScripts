# !/usr/bin/env python
# -*- coding: utf-8 -*

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# pre_configured setup files
from conf import*



def bayleys(url):
    pass
def mainRunner():
    bayleys('https://www.bayleys.co.nz/search?SearchType=Residential&Radius=6&ListingType=None&OrderType=LatestListing&Page=1&KeywordIsListingId=False&TabType=Properties&ViewType=Gallery&AuctionsOnly=False&PageSize=12')


def init_db():
    logger.debug("initializing database")
    c = DB.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'Residential_Extract'")
    if c.fetchone() is None:
        logger.debug('create database')
        c.execute("""
           CREATE TABLE justcars_links
       (
            id integer PRIMARY KEY,
            link text NOT NULL,
            listing_id text,
            json blob
        )      
        """)

def main():
    if test_ip():
        mainRunner()




if __name__ == "__main__":
    main()