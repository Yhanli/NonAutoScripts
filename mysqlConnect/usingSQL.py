import mysql.connector
import json

# this can only use accessed within the local network
mydb = mysql.connector.connect(
    host = "rm-j0bdbh63j18z1ajrm.mysql.australia.rds.aliyuncs.com",
    user = "test3",
    port = 3306,
    passwd = "6p9TriavDyvNFhqpnw",
    database="test_oneroof"
)



mycursor = mydb.cursor(dictionary=True)

mycursor.execute('SELECT * FROM builder_franchise')
result = mycursor.fetchall()

# print(result)
result_list = []
for i in result:
    mycursor.execute('select name from builder_brand where id = {0}'.format(i['brand_id']))
    company = mycursor.fetchone()
    print(company)
    office_details_sample = {
        'url':i['website'],
        'company':company,
        'office':i['name'],
        'phone':i['phone'],
        'email':i['email'],
        'address':i['address'],
        'open_hours':'',
        'about_us':i['bio'],
        "avatar":'https://s.oneroof.co.nz/image/{0}/{1}/{3}'.format(i['ossImageLogo'][:2],i['ossImageLogo'][2:4],i['ossImageLogo']),
        "google_coordinate":""}
    result_list.append(office_details_sample)

with open('franchise.json', 'w+') as fp:
    json.dump({"data":result_list},fp)