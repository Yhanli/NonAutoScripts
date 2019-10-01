#%%
# !/usr/bin/env python
# -*- coding: utf-8 -*

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time,random
import csv

# pre_configured setup files
from conf import *

executor = ThreadPoolExecutor(max_workers=4)


def CompareExport():

    with open('listings.csv', 'r', encoding='utf-8') as fp:
        csv_file = fp.read()
    dataCSV = list()
    c = DB.cursor()
    c.execute('SELECT * FROM Residential_Extract_duplicate')
    all_listings = c.fetchall()
    for listing in all_listings:
        listing_url = listing[1]
        listing_number = listing[2]
        listing_address = listing[3]
        listing_title = listing[4]
        if listing_number.strip() + '|' in csv_file:
            exist = 'Yes'
        else:
            exist = 'No'
        dataCSV.append([listing_url, listing_number,listing_address,listing_title,exist])
    with open('Compared.csv', 'w+') as csvfile:
        csvwriter = csv.writer(csvfile, lineterminator = '\n')
        csvwriter.writerows(dataCSV)

def remove_duplicate():
    c = DB.cursor()
    c.execute('SELECT * FROM Residential_Extract')
    All_Listing = c.fetchall()

    listing_dic = {}

    for listing in All_Listing:
        listing_dic[listing[1]] = listing
    logger.debug(listing_dic)

    for key,val in listing_dic.items():
        logger.debug('processing %s'%key)
        listing_url = val[1]
        listing_number = val[2]
        listing_address = val[3]
        listing_title = val[4]
        c.execute('INSERT INTO Residential_Extract_duplicate (link,listing_id,listing_address,listing_title) VALUES (?,?,?,?)',(listing_url, listing_number,listing_address,listing_title))
    DB.commit()

def raywhite(url):
    count = 0
    while url != None:
        url = Get_Raywhite_Main(url,count)
        count += 1
        # break

def Get_Raywhite_Main(url, page):
    DB = sqlite3.connect(currentDir + '/data.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    logger.debug('http://raywhite.co.nz/Residential_Property ==>currently on page %s'%page)
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
    # testwrite(response.content)
    soup = GetBSsoup(response)
    c = DB.cursor()

    links = soup.find_all('div', class_='galleryViewBox')
    insert_item = []
    for link in links:
        listing_url = link.find('a').get('href')
        listing_number = link.find('a').get('href').split('/')[-1]
        try:
            listing_address = link.find('p').text.split(',')[1].strip().replace('...','') + ', ' + link.find('p').text.split(',')[0]
        except:
            listing_address = ''
        try:
            listing_title = link.find('h3').text
        except:
            listing_title = ''
        # print((listing_url, listing_number,listing_address,listing_title))
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
    DB = sqlite3.connect(currentDir + '/data.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    response = requests.get(url, headers=random.choice(header), proxies = random.choice(proxies))
    # testwrite(response.content)
    soup = GetBSsoup(response)
    c = DB.cursor()
    try:
        next_page = 'https://www.barfoot.co.nz/properties/residential/'+ soup.find('div',attrs={'class':'button secondary-button next'} ).get('onclick').split('/')[-1][:-1] #PagedList-skipToNext right-etc
    except Exception as e:
        logger.debug(str(e))
        return None
    logger.debug(next_page)
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
        # print((listing_url, listing_number,listing_address,listing_title))
        c.execute('INSERT INTO Residential_Extract (link,listing_id,listing_address,listing_title) VALUES (?,?,?,?)',(listing_url, listing_number,listing_address,listing_title))
    DB.commit()
    return next_page


def bayleys(url):
    while url != None:
        url = Get_Bayley_Main(url)
def Get_Bayley_Main(url):
    DB = sqlite3.connect(currentDir + '/data.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
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

def init_db():
    DB = sqlite3.connect(currentDir + '/data.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
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
    c.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'Residential_Extract_duplicate'")
    if c.fetchone() is None:
        logger.debug('create database')
        c.execute("""
           CREATE TABLE Residential_Extract_duplicate
       (
            id integer PRIMARY KEY,
            link text NOT NULL,
            listing_id text,
            listing_address text,
            listing_title text,
            json blob
        )      
        """)

def mainRunner():
    if mode == '1':
        executor.submit(bayleys,'https://www.bayleys.co.nz/search?SearchType=Residential&Radius=6&ListingType=None&OrderType=LatestListing&Page=1&KeywordIsListingId=False&TabType=Properties&ViewType=Gallery&AuctionsOnly=False&PageSize=12')
        executor.submit(barfoot,'https://www.barfoot.co.nz/properties/residential/page=1')
        executor.submit(raywhite,'http://raywhite.co.nz/Residential_Property')
        executor.shutdown(wait=True)
        remove_duplicate()
    elif mode == '2':
        CompareExport()
    else:
        executor.submit(bayleys,'https://www.bayleys.co.nz/search?SearchType=Residential&Radius=6&ListingType=None&OrderType=LatestListing&Page=1&KeywordIsListingId=False&TabType=Properties&ViewType=Gallery&AuctionsOnly=False&PageSize=12')
        executor.submit(barfoot,'https://www.barfoot.co.nz/properties/residential/page=1')
        executor.submit(raywhite,'http://raywhite.co.nz/Residential_Property')
        executor.shutdown(wait=True)
        remove_duplicate()
        CompareExport()


def main():
    if test_ip():
        init_db()
        mainRunner()


if __name__ == "__main__":
    main()