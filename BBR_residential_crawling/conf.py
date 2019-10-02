# !/usr/bin/env python
# -*- coding: utf-8 -*
import sqlite3,os,sys,logging,requests, random
from bs4 import BeautifulSoup

currentDir = os.path.dirname(os.path.realpath(__file__))
try:
    mode = sys.argv[1]
except:
    mode = '100'
print('Mode %s'%mode)

# DB = sqlite3.connect(currentDir + '/data.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
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

with open('/usr/local/services/spider/conf/proxies.txt', 'r') as proFile:   #currentDir + '/conf/proxies.txt'
    proxies = [i.replace('\n', '').replace('\r', '') for i in proFile.readlines()]
    proxies = ['http://' + i.split(':')[2] + ':' + i.split(':')[3] + '@' + i.split(':')[0] + ':' + i.split(':')[1] for i
               in proxies]
    proxies = [{'http': i, 'https': i} for i in proxies]

proxies = [proxies[1]]
headers = [header[0]]

with open('/usr/local/services/spider/conf/sendgrid_key', 'r') as fp:
    key = fp.read()

def testwrite(data):
    try:
        with open(currentDir + '/testwrite.html','wb+') as fp:
            fp.write(data)
    except:
        with open(currentDir + '/testwrite.txt','w+') as fp:
            fp.write(data)

def clear_db(DB,table):
    try:
        c = DB.cursor()
        c.execute("DELETE FROM %s"%table)
        DB.commit()
    except Exception as e:
        logger.debug('Failed to clear DB, %s'%str(e))

def test_ip():
    global proxies
    proxy = random.choice(proxies)
    header = random.choice(headers)
    url = 'https://whatismyipaddress.com/'
    response = requests.get(url, headers=header, proxies = proxy)
    checked = ('IP == Proxy =========>>>{0} --------- {1}'.format(str(proxy).split('@')[-1].split(':')[0] in str(response.text),str(proxy).split('@')[-1].split(':')[0]))
    logger.debug(checked)
    return True if 'True' in checked else False


def GetUrlContent(url = '',useProxy = True):
    try:
        if useProxy:
            return requests.get(url, headers=random.choice(header), proxies = random.choice(proxies), timeout = 10)
        else:
            return requests.get(url, timeout = 10)
    except Exception as e :
        logger.debug('Error occur when requesting url: {url}:{error}'.format(url=url, error=str(e)) )
        return ('Error occur when requesting url: {url}:{error}'.format(url=url, error=str(e)) )

def GetBSsoup(response):
    return BeautifulSoup(response.text, features='lxml')
# will not need to set up currentDir, data.db will always be generated with types enable, loaded proxies, common headers
