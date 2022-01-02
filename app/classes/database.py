# packages
import os
from dotenv import load_dotenv
from mysql.connector import connect, Error
from datetime import datetime

# load environment vars
load_dotenv()

# Binance
class Database:

    def __init__(self, 
                    hostname=os.getenv('MYSQL_HOSTNAME'), 
                    username=os.getenv('MYSQL_USERNAME'), 
                    password=os.getenv('MYSQL_PASSWORD'),
                    database=os.getenv('MYSQL_DATABASE')):

        try:
            with connect(
                host=hostname,
                user=username,
                password=password,
                database=database,
            ) as connection:

                self.host = hostname
                self.user = username
                self.password = password
                self.database = database

        except Error as e:
            print(e)
            exit(-1)
    
    def getClient(self):
        return connect(host=self.host, user=self.user, password=self.password, database=self.database)

    def fetchAll(self, table):
        mydb = self.getClient()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM " + table)
        myresult = mycursor.fetchall()

        return myresult

    def fetchFirst(self, table, item_id):
        mydb = self.getClient()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM " + table + " WHERE id = " + str(item_id))
        myresult = mycursor.fetchone()

        return myresult

    def query(self, query):
        mydb = self.getClient()
        mycursor = mydb.cursor()
        mycursor.execute(query)
        mydb.commit()

    def insertCandles(self, id_token, id_interval, candles):
 

        query = "INSERT INTO candles (id_token, id_interval, open, high, low, close, volume_coin_1, volume_coin_2, open_time, close_time, open_at, close_at) VALUES "

        for candle in candles:

            # variables
            open_time = str(candle["open_time"])
            close_time = str(candle["close_time"])
            open_time = open_time[:-3]   # remove last 3 digits
            close_time = close_time[:-3] # remove last 3 digits
            open_at = str(datetime.fromtimestamp(int(open_time)))
            close_at = str(datetime.fromtimestamp(int(close_time)))

            # item
            item = []
            item.append(str(id_token))
            item.append(str(id_interval))
            item.append(str(candle["open"]))
            item.append(str(candle["high"]))
            item.append(str(candle["low"]))
            item.append(str(candle["close"]))
            item.append(str(candle["volume_coin_1"]))
            item.append(str(candle["volume_coin_2"]))
            item.append(open_time)
            item.append(close_time)
            item.append('"' + open_at + '"')
            item.append('"' + close_at + '"')

            # line
            line = ", ".join(item)
            line = "(" + line + "), "

            query = query + "\n " + line

        # remove lastest 2 chars
        query = query[:-2]

        # execute
        self.query(query)



    def getTokens(self):
        return self.fetchAll("tokens")

    def getIntervals(self):
        return self.fetchAll("intervals")

    def getTasks(self):
        return self.fetchAll("tasks")

    def getToken(self, item_id):
        return self.fetchFirst("tokens", item_id)

    def getInterval(self, item_id):
        return self.fetchFirst("intervals", item_id)

    def completeTask(self, id_task):
        self.query("UPDATE tasks SET executed = true WHERE id = " + str(id_task))

    def removeCandles(self, id_token, id_interval):
        self.query("DELETE FROM candles WHERE id_token = " + str(id_token) + " AND id_interval = " + str(id_interval))

