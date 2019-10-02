import csv

import urllib.request


urllib.request.urlretrieve('https://hougarden-img.oss-ap-southeast-2.aliyuncs.com/crawler_conf/listings_hou.csv','/tmp/listings_hou.csv')
urllib.request.urlretrieve('https://hougarden-img.oss-ap-southeast-2.aliyuncs.com/crawler_conf/listings_one.csv','/tmp/listings_one.csv')

with open('/tmp/listings_hou.csv', 'r', encoding='utf-8') as fp:
    csv_file_hou = fp.read()
with open('/tmp/listings_one.csv', 'r', encoding='utf-8') as fp:
    csv_file_one = fp.read()

towrite = list()
with open('Compared.csv', 'r', encoding='utf-8') as fp:
    csvReader = csv.reader(fp, lineterminator = '\n')

    for row in csvReader:
        company = row[0].split('www.')[-1].split('.co')[0]
        listing_num = row[1]
        if listing_num +'|' in csv_file_one:
            on_one = 'Yes'
        else:
            on_one = 'No'
        towrite.append([company] + row + [on_one])
        print(row[0])

with open('Compared_with_one.csv', 'w+') as csvfile:
    csvwriter = csv.writer(csvfile, lineterminator = '\n')
    csvwriter.writerow(['company','url', 'listingNo', 'ListingAddr', 'ListingTittle','ExistOnHougarden', 'ExistOnOneroof'])
    csvwriter.writerows(towrite)

    