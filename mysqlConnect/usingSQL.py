import mysql.connector


# this can only use accessed within the local network
mydb = mysql.connector.connect(
    host = "rm-j0bdbh63j18z1ajrm.mysql.australia.rds.aliyuncs.com",
    user = "test3",
    port = 3306,
    passwd = "6p9TriavDyvNFhqpnw",
    database="test_oneroof"
)

mycursor = mydb.cursor()

mycursor.execute('SELECT id, name FROM builder_franchise')

result = mycursor.fetchall()
for i in result:
    print(i)
