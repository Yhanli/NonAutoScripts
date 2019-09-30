# !/usr/bin/env python
# -*- coding: utf-8 -*
import sqlite3,os,sys,logging

currentDir = os.path.dirname(os.path.realpath(__file__))
try:
    mode = sys.argv[1]
except:
    mode = '100'
print('Mode %s'%mode)

DB = sqlite3.connect(currentDir + '/data.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

header = [
    {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'origin': 'https://wallstreetcn.com',
    'Referer': 'https://wallstreetcn.com/vip/articles/3476537'},
    {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.1 Safari/605.1.15'},
    {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'},
    {'user-agent': 'Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18'},
    {'user-agent': 'Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)'}]  # headers

currentDir = os.path.dirname(os.path.realpath(__file__))
with open('/data/Scripts/conf/proxies.txt', 'r') as proFile:   #currentDir + '/conf/proxies.txt'
    proxies = [i.replace('\n', '').replace('\r', '') for i in proFile.readlines()]
    proxies = ['http://' + i.split(':')[2] + ':' + i.split(':')[3] + '@' + i.split(':')[0] + ':' + i.split(':')[1] for i
               in proxies]
    proxies = [{'http': i, 'https': i} for i in proxies]

proxies = [proxies[1]]
header = [header[0]]
