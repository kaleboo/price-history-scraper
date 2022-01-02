# packages
import time

# classes
from classes.binance import Binance
from classes.amazon import Amazon
from classes.database import Database
from classes.helper import Helper

# clients
binance = Binance()
database = Database()

# tasks
tokens = database.getTokens()
intervals = database.getIntervals()

# header
print("INSERT INTO `tasks` (id_token, id_interval, description, executed) VALUES")

# loop(s)
for token in tokens:

    for interval in intervals:

        print("(" + str(token[0]) + ", " + str(interval[0]) + ", '" + str(token[2]) + "_" + str(interval[1]) + "', false),")
