# packages
import time

# classes
from classes.binance import Binance
from classes.amazon import Amazon
from classes.database import Database
from classes.helper import Helper

# Check if this process is already on execution
if Helper.isRunning():
	print("There is another process on execution")
	exit(-1)

# Flag this process
Helper.runningFlag()

# Max tasks to be executed
MAX_TASKS = 1
proccesed = 0

# clients
binance = Binance()
database = Database()

# tasks
tasks = database.getTasks()

for task in tasks:

	# Check if is already proccessed
	executed = task[4]
	if executed:
		print("[task] " + str(task[0]) + " already executed.")
		continue

	# ids
	id_token = task[1]
	id_interval = task[2]

	# Models
	token = database.getToken(id_token)
	interval = database.getInterval(id_interval)

	# Ids
	pair = token[2]
	temporality = interval[1]

	# candles for first token
	candles = binance.getCandles(pair, temporality)

	# output
	filepath = "output/" + pair + "_" + temporality + ".csv"

	# export
	Helper.writeCSV(candles, filepath)

	# log
	print("[" + pair + "] " + filepath + " successfully created.")

	# mysql save
	database.removeCandles(id_token, id_interval)
	database.insertCandles(id_token, id_interval, candles)

	# update tasks
	database.completeTask(task[0])

	# update proccesed counter
	proccesed = proccesed + 1

	# check max_tasks
	if proccesed == MAX_TASKS:

		# clean
		helper.removeRunningFlag()

		# bye!
		print("[task] maximum of tasks successfully executed.")
		break

	# pause
	time.sleep(60)



print("done.")
