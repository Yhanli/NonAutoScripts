# !/usr/bin/env python
# -*- coding: utf-8 -*
import sqlite3, os, sys, logging, requests, random
from bs4 import BeautifulSoup, re

currentDir = os.path.dirname(os.path.realpath(__file__))
try:
    mode = sys.argv[1]
except:
    mode = "100"
print("Mode %s" % mode)

# DB = sqlite3.connect(currentDir + '/data.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

header = [
    {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "origin": "https://wallstreetcn.com",
        "Referer": "https://wallstreetcn.com/vip/articles/3476537",
    },
    {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.1 Safari/605.1.15"
    },
    {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"
    },
    {"user-agent": "Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18"},
    {"user-agent": "Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)"},
]  # headers

with open(
    "/usr/local/services/spider/conf/proxies.txt", "r"
) as proFile:  # currentDir + '/conf/proxies.txt'
    proxies = [i.replace("\n", "").replace("\r", "") for i in proFile.readlines()]
    proxies = [
        "http://"
        + i.split(":")[2]
        + ":"
        + i.split(":")[3]
        + "@"
        + i.split(":")[0]
        + ":"
        + i.split(":")[1]
        for i in proxies
    ]
    proxies = [{"http": i, "https": i} for i in proxies]

proxies = [proxies[0]]
headers = [header[0]]

with open("/usr/local/services/spider/conf/sendgrid_key", "r") as fp:
    key = fp.read()


def testwrite(data):
    # return
    try:
        with open(currentDir + "/testwrite.html", "wb+") as fp:
            fp.write(data)
    except:
        with open(currentDir + "/testwrite.html", "w+") as fp:
            fp.write(data)


def clear_db(DB, table):
    try:
        c = DB.cursor()
        c.execute("DELETE FROM %s" % table)
        DB.commit()
    except Exception as e:
        logger.debug("Failed to clear DB, %s" % str(e))


def test_ip():
    global proxies
    proxy = random.choice(proxies)
    header = random.choice(headers)
    url = "https://whatismyipaddress.com/"
    response = requests.get(url, headers=header, proxies=proxy)
    checked = "IP == Proxy =========>>>{0} --------- {1}".format(
        str(proxy).split("@")[-1].split(":")[0] in str(response.text),
        str(proxy).split("@")[-1].split(":")[0],
    )
    logger.debug(checked)
    return True if "True" in checked else False


def GetUrlContent(url="", useProxy=True):
    for i in range(2):
        try:
            if useProxy:
                return requests.get(
                    url,
                    headers=random.choice(header),
                    proxies=random.choice(proxies),
                    timeout=10,
                    allow_redirects=True,
                )
            else:
                return requests.get(url, timeout=10, allow_redirects=True)
            break
        except Exception as e:
            logger.debug(
                "Error occur when requesting url: {url}:{error}".format(
                    url=url, error=str(e)
                )
            )
            if i >= 1:
                return "Error occur when requesting url: {url}:{error}".format(
                    url=url, error=str(e)
                )


def GetBSsoup(response_content):
    return BeautifulSoup(response_content, features="lxml")


def get_openTime(date_string):
    ##### day
    final_time_list = []
    string_lower = date_string.lower()
    final_time_list = []

    if "7 day" in string_lower or "everyday" in string_lower or "7day" in string_lower:
        for i in range(1,8):
            final_time_list.append(
                {"weekday": str(i), "start_time": "", "end_time": ""}
            )
            string_lower = string_lower.replace("7 day", "")
            string_lower = string_lower.replace("7day", "")
            string_lower = string_lower.replace("everyday", "")

    elif "-" in string_lower or "to" in string_lower:
        toggle = 0
        start = ""
        end = ""
        weekday_list = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        dic_weekday = {
            "mon": 1,
            "tue": 2,
            "wed": 3,
            "thu": 4,
            "fri": 5,
            "sat": 6,
            "sun": 7,
        }
        for a in re.sub("[^a-z0-9.:]", " ", string_lower).split(" "):
            for i in weekday_list:
                if i in a:
                    if toggle == 0:
                        start = dic_weekday[i]
                        toggle = 1
                        string_lower = string_lower.replace(i, "")
                    else:
                        end = dic_weekday[i]
                        string_lower = string_lower.replace(i, "")

        if start < end:
            for i in range(start, end + 1):
                final_time_list.append({"weekday": i, "start_time": "", "end_time": ""})
        elif end < start:
            for i in range(start, 8):
                final_time_list.append({"weekday": i, "start_time": "", "end_time": ""})
            for i in range(1, end + 1):
                final_time_list.append({"weekday": i, "start_time": "", "end_time": ""})

    else:
        if "mon" in re.sub("[^a-z0-9]", "", string_lower):
            final_time_list.append({"weekday": 1, "start_time": "", "end_time": ""})
        if "tue" in re.sub("[^a-z0-9]", "", string_lower):
            final_time_list.append({"weekday": 2, "start_time": "", "end_time": ""})
        if "wed" in re.sub("[^a-z0-9]", "", string_lower):
            final_time_list.append({"weekday": 3, "start_time": "", "end_time": ""})
        if "thu" in re.sub("[^a-z0-9]", "", string_lower):
            final_time_list.append({"weekday": 4, "start_time": "", "end_time": ""})
        if "fri" in re.sub("[^a-z0-9]", "", string_lower):
            final_time_list.append({"weekday": 5, "start_time": "", "end_time": ""})
        if "sat" in re.sub("[^a-z0-9]", "", string_lower):
            final_time_list.append({"weekday": 6, "start_time": "", "end_time": ""})
        if "sun" in re.sub("[^a-z0-9]", "", string_lower):
            final_time_list.append({"weekday": 7, "start_time": "", "end_time": ""})

    ###### time
    date_string = string_lower.replace(":00", "-").replace(".00", "-")
    time_list = [s for s in re.sub("[^0-9:.]", "-", date_string).split("-") if s != ""]
    start_time = 0
    end_time = 0
    toggle = 0

    for i in time_list:
        try:
            i = int(i)
        except:
            continue
        if i > 7 and toggle == 0:
            start_time = i
            toggle = 1
        if i < 4 and toggle == 0:
            start_time = i + 12
            toggle = 1
        elif i < 12 and toggle != 0 and i < start_time:
            end_time = i + 12
        elif i <= 12 and toggle != 0:
            end_time = i

    if start_time > end_time:
        tmp = end_time
        end_time = start_time
        start_time = tmp

    if start_time < 12:
        start_time = str(start_time) + "am"
    else:
        if start_time == 12:
            start_time = str(start_time) + "pm"
        else:
            start_time = str(start_time - 12) + "pm"
    if end_time < 12:
        end_time = str(end_time) + "am"
    else:
        if end_time == 12:
            end_time = str(end_time) + "pm"
        else:
            end_time = str(end_time - 12) + "pm"

    return_time = []
    for i in final_time_list:
        i["start_time"] = start_time
        i["end_time"] = end_time
        return_time.append(i)

    return return_time


# will not need to set up currentDir, data.db will always be generated with types enable, loaded proxies, common headers

