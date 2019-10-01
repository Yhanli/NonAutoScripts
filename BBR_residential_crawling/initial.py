#%%
# !/usr/bin/env python
# -*- coding: utf-8 -*

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time,random

# pre_configured setup files
from conf import *




def raywhite(url):
    count = 112
    while url != None:
        url = Get_Raywhite_Main(url,count)
        count += 1
        # break

def Get_Raywhite_Main(url, page):
    logger.debug('currently on page %s'%page)
    data = {}
    if page != 0:
        data = {
            'currentPageIndex': '{page}'.format(page = page),
            'gotoPage': '{page_plus}'.format(page_plus = page+1),
            'sort': 'Highest Price',
            'form': 'listingForm',
            'layout': 'GRID',
            'updateLayout': '0',
            'tab': 'Residential',
            'keyword': '',
            'isFromSRP': '1',
            'maxPageIndex': '348',
            'orderBy': 'Highest Price'
        }
    response = requests.get(url, headers=random.choice(header), proxies = random.choice(proxies), data = data)
    testwrite(response.content)
    soup = GetBSsoup(response)
    c = DB.cursor()

    links = soup.find_all('div', class_='galleryViewBox')
    insert_item = []
    for link in links:
        listing_url = link.find('a').get('href')
        listing_number = link.find('a').get('href').split('/')[-1]
        listing_address = link.find('p').text.split(',')[1].strip().replace('...','') + ', ' + link.find('p').text.split(',')[0]
        try:
            listing_title = link.find('h3').text
        except:
            listing_title = ''
        print((listing_url, listing_number,listing_address,listing_title))
        c.execute('INSERT INTO Residential_Extract (link,listing_id,listing_address,listing_title) VALUES (?,?,?,?)',(listing_url, listing_number,listing_address,listing_title))
    DB.commit()
    if '>Next &gt;</span>' not in str(soup):
        return None
    else:
        return url

def barfoot(url):
    while url != None:
        url = Get_Barfoot_Main(url)
        
def Get_Barfoot_Main(url):
    response = requests.get(url, headers=random.choice(header), proxies = random.choice(proxies))
    testwrite(response.content)
    soup = GetBSsoup(response)
    c = DB.cursor()
    try:
        next_page = 'https://www.barfoot.co.nz/properties/residential/'+ soup.find('div',attrs={'class':'button secondary-button next'} ).get('onclick').split('/')[-1][:-1] #PagedList-skipToNext right-etc
    except Exception as e:
        logger.debug(str(e))
        return None
    print(next_page)
    links = soup.find_all('a', class_='property-link')
    insert_item = []
    for link in links:
        listing_url = 'https://www.barfoot.co.nz'+ link.get('href')
        listing_number = link.get('href').split('/')[-1]
        listing_address = link.find('div').text
        # try:
        #     # listing_title = soup.find('a', attrs={'title':'View  listing #{0} with more detail'.format(listing_number)}).text.strip()
        # except:
        listing_title = ''
        print((listing_url, listing_number,listing_address,listing_title))
        c.execute('INSERT INTO Residential_Extract (link,listing_id,listing_address,listing_title) VALUES (?,?,?,?)',(listing_url, listing_number,listing_address,listing_title))
    DB.commit()
    return next_page


def bayleys(url):
    while url != None:
        url = Get_Bayley_Main(url)
def Get_Bayley_Main(url):
    response = requests.get(url, headers=random.choice(header), proxies = random.choice(proxies))
    # testwrite(response.content)
    soup = GetBSsoup(response)
    c = DB.cursor()
    try:
        next_page = 'https://www.bayleys.co.nz'+ soup.find('li',attrs={'class':'PagedList-skipToNext'} ).find('a').get('href').replace('&amp;','&') #PagedList-skipToNext right-etc
    except Exception as e:
        logger.debug(str(e))
        return None
    links = soup.find_all('a', class_='embed-responsive embed-responsive-listing-thumbnail')
    insert_item = []
    for link in links:
        listing_url = 'https://www.bayleys.co.nz'+ link.get('href')
        listing_number = link.get('href').split('/')[-1]
        listing_address = link.get('title')
        try:
            listing_title = soup.find('a', attrs={'title':'View  listing #{0} with more detail'.format(listing_number)}).text.strip()
        except:
            listing_title = ''

        c.execute('INSERT INTO Residential_Extract (link,listing_id,listing_address,listing_title) VALUES (?,?,?,?)',(listing_url, listing_number,listing_address,listing_title))
    DB.commit()
    return next_page

def mainRunner():
    # bayleys('https://www.bayleys.co.nz/search?SearchType=Residential&Radius=6&ListingType=None&OrderType=LatestListing&Page=1&KeywordIsListingId=False&TabType=Properties&ViewType=Gallery&AuctionsOnly=False&PageSize=12')
    # barfoot('https://www.barfoot.co.nz/properties/residential/page=1')
    raywhite('http://raywhite.co.nz/Residential_Property')

def init_db():
    logger.debug("initializing database")
    c = DB.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'Residential_Extract'")
    if c.fetchone() is None:
        logger.debug('create database')
        c.execute("""
           CREATE TABLE Residential_Extract
       (
            id integer PRIMARY KEY,
            link text NOT NULL,
            listing_id text,
            listing_address text,
            listing_title text,
            json blob
        )      
        """)


def main():
    if test_ip():
        init_db()
        mainRunner()




if __name__ == "__main__":
    main()