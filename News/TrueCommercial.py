# !/usr/bin/env python
# -*- coding: utf-8 -*


from conf import *
from datetime import datetime, timedelta
import copy, hashlib, oss2, json

json_raw = {
    "title": "",
    "author": "",
    "site_name": "",
    "publish_date": "",
    "cover": "",
    "brief": "",
    "news_category": "",
    "comments": [],
    "rawhtml": "",
    "cleanhtml": ""
}
with open(currentDir + '/' + 'oss_auth', 'r') as Afile:
    data = Afile.read().split('\n')
auth = oss2.Auth(data[0], data[1])
bucket = oss2.Bucket(auth, data[2], data[3], enable_crc=False)
bucketSrc = 'https://s.hougarden.com/'
bucketSrcEnd = '?x-oss-process=image/quality,q_80'

next_page = False

def get_news_body(url, json_data, count):
    resp = GetUrlContent(url)
    data = GetBSsoup(resp.text)
    news_body = data.find('div', attrs={'class': 'content-container'})
    json_data["author"] = news_body.find('span', class_="author").text if "True Commercial" not in news_body.find('span', class_="author").text else ""
    json_data["site_name"] = "True Commercial"
    json_data["title"] = news_body.find('h1').text

    date_time = news_body.find("span", class_="date").text
    print(date_time)
    json_data["publish_date"] = datetime.strptime(date_time, "%H:%M %p %A %B %d, %Y").strftime("%Y-%m-%d %H:%M:%S")

    contents = news_body.find_all('p')
    contents += news_body.find_all('div')
    cover = upload_img_oss("http://truecommercial.oneroof.co.nz" + news_body.find('img').get("src"))
    json_data["cover"] = cover[-1]
    for p in contents:
        if "Photo / Supplied" in str(p) or "feature-image" in str(p) or "span class" in str(p) or "<h1>" in str(p):
            continue
        json_data["cleanhtml"] = json_data["cleanhtml"] + str(p)

    json_data["cleanhtml"] = '<font color="#000000">' + json_data["cleanhtml"] + '</font>'
    print(json_data["title"], cover[0])
    with open('extract/%s.json'%count, 'w+') as fp:
        json.dump(json_data, fp, ensure_ascii=False)


def upload_img_oss(img_link):
    imgMD5 = str(hashlib.md5(img_link.encode('utf-8')).hexdigest())
    bucketDir = 'article/' + \
                imgMD5[:2] + '/' + imgMD5[2:4] + '/'
    imgType = '.jpg'
    fullDir = bucketDir + imgMD5 + imgType

    response = requests.get(img_link.strip())
    bucket.put_object(fullDir, response.content)
    return [bucketSrc + fullDir + bucketSrcEnd, imgMD5 + imgType]

def get_news():
    while True:
        link = "http://truecommercial.oneroof.co.nz/insights/news/?news=0&p=1&pp=799"

        response = GetUrlContent(link)
        testwrite(response.content)
        data = GetBSsoup(response.content)

        content_list = data.find_all('div', attrs={"class":"news-list-content"})
        count = 1
        for item in content_list:
            try:
                date = item.find("p", class_= "date").text.replace("Date ", "")
                strTodate = datetime.strptime(date, "%b %Y")
                if strTodate > datetime.now() - timedelta(days=190):
                    newslink = ("http://truecommercial.oneroof.co.nz" + item.find("a").get('href'))
                    json_item = copy.deepcopy(json_raw)
                    json_item["publish_date"] = strTodate.strftime("%Y-%m-%d")
                    json_item["news_category"] = "commercial"
                    json_item["original"] = newslink
                    json_item["brief"] = item.text.replace(item.find('h3').text, "").replace(item.find("p", class_= "date").text, "").replace("more", "").strip()
                    get_news_body(url = newslink, json_data = json_item, count = str(count))

                    count += 1
            except Exception as e:
                print(str(e))
                continue


        if not next_page:
            break

def combine():
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(currentDir + '/extract') if isfile(join(currentDir + '/extract', f))]
    onlyfiles.sort()
    final = []

    for i in onlyfiles:
        if ".D" in i:
            continue
        with open("extract/%s"%i) as fp:
            data = json.load(fp)
            final.append(data)
        os.remove("extract/%s"%i)

    with open("TrueCommercial.json", 'w+') as fp:
        json.dump({"data":final}, fp, ensure_ascii=False)

get_news()
combine()