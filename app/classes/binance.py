# packages
import os
import time

from dotenv import load_dotenv
from binance import Client
from classes.helper import Helper

# load environment vars
load_dotenv()

# Binance
class Binance:

    # constructor
    def __init__(self, apikey=os.getenv('BINANCE_API_KEY'), secretkey=os.getenv('BINANCE_SECRET_KEY')):

        # keep some arguments
        self.apikey = apikey
        self.secretkey = secretkey

        # instance the client
        self.client = Client(self.apikey, self.secretkey)


    # get exchange info
    def getExchangeInfo(self):

        # api
        info = self.client.get_exchange_info()

        # bye
        return info



    # get latest price for given pair
    def getPrice(self, pair):

        # api
        info = self.client.get_avg_price(symbol=pair)

        # append the requested pair
        info["pair"] = pair

        # bye
        return info


    # get all available coins in binance.
    def getCoins(self, filter=""):
        
        # api
        coins = self.client.get_all_tickers()

        # is it neccesary to filter?
        if filter=="":
            return coins

        # filter
        pairs = []
        for coin in coins:
            # si termina con XXX y no tiene BULL ni tiene BEAR
            if coin["symbol"].endswith(filter) and "BEAR" not in coin["symbol"] and "BULL" not in coin["symbol"]:
                pairs.append(coin["symbol"])
        
        # bye
        return pairs


    # get candle information
    def getCandle(self, pair, interval):

        # api
        candles = self.client.get_klines(symbol=pair, interval=interval)

        # skip
        if len(candles) < 100:
            return None

        # latest
        candle = candles[-1]
        candle2 = candles[-2]

        # volatility
        volatility = Helper.getVolatility(candle[2], candle[3], candle2[2], candle2[3])

        # custom object
        item = {
          "pair": pair,
          "interval": interval,
          "open": Helper.formatNumber(candle[1]),
          "high": Helper.formatNumber(candle[2]),
          "low": Helper.formatNumber(candle[3]),
          "close": Helper.formatNumber(candle[4]),
          "volume_coin_1": Helper.formatNumber(candle[5]),
          "volume_coin_2": Helper.formatNumber(candle[7]),
          "volatility": volatility,
          "open_time": int(candle[0]),
          "close_time": int(candle[6])
        }

        # bye
        return item


    # get candles
    def getCandles(self, pair, interval):

        # execution time
        start_time = time.time()

        # validate
        if not Helper.isValidInterval(interval):
            print("invalid " + interval + " interval.")
            exit(-1)

        # Initial Date: Jan. 1st, 2021 00:00:00
        initial_date = 1609459200

        # Ending Date: Jan. 1st, 2022 00:00:00
        ending_date = 1640995200

        # we have to wait 1 min after 500 requests
        max_requests = 500

        # seconds multiplier
        seconds = Helper.intervalToSeconds(interval)

        # candles
        candles = int((ending_date - initial_date) / seconds)

        # loops (we get 1,000 per request)
        loops = int(candles / 1000) + 1

        # counter for requests
        requests = 0

        # information
        print("[" + pair + "_" + interval + "] There is " + str(candles) + " candles in 2021 for given " + interval + " interval")
        print("[" + pair + "_" + interval + "] This requires " + str(loops) + " requests")


        # list
        items = []

        # go go go!
        for i in range(loops):

            # sleep if neccesary
            if (requests == 500):
                time.sleep(60)
                requests = 0

            # starting date
            starting_loop_date = initial_date + (i * seconds * 1000)
            starting_loop_date_miliseconds = starting_loop_date * 1000

            ending_loop_date = initial_date + ((i+1) * seconds * 1000) - 1

            # api
            candles = self.client.get_klines(symbol=pair, interval=interval, limit=1000, startTime=starting_loop_date_miliseconds)

            # iterate
            for candle in candles:

                # custom object
                item = {
                  "pair": pair,
                  "interval": interval,
                  "open": Helper.formatNumber(candle[1], 8),
                  "high": Helper.formatNumber(candle[2], 8),
                  "low": Helper.formatNumber(candle[3], 8),
                  "close": Helper.formatNumber(candle[4], 8),
                  "volume_coin_1": Helper.formatNumber(candle[5], 8),
                  "volume_coin_2": Helper.formatNumber(candle[7], 8),
                  "open_time": int(candle[0]),
                  "close_time": int(candle[6])
                }

                # ignore if is it an outlier
                open_time = int(candle[0]) / 1000

                if open_time >= ending_date:
                    break

                if open_time < starting_loop_date or open_time > ending_loop_date:
                    break

                # append
                items.append(item)

            progress = round(((i + 1) / loops) * 100, 2)
            print("[" + pair + "_" + interval + "] loop: " + str(i + 1) + " candles: " + str(len(items)) + " progress: " + str(progress) + "%")

            # update
            requests = requests + 1

        # execution time
        print("--- %s seconds ---" % (time.time() - start_time))

        return items


    # get list of coins and append to each one the latest candle
    def getCoinsWithCandle(self, filter = ""):
        
        # get coins
        coins = self.getCoins(filter)

        # result var
        items = []

        # iterate over each coin
        for coin in coins:

            # get the latest candle
            candle = self.getCandle(coin, "1d")
            if (candle is not None) and (candle["volatility"] > 1.00) and (candle["volume_coin_2"] > 100000):
                candle["tier"] = Helper.getTier(candle["volume_coin_2"])
                items.append(candle)

            # progress
            print(coin + " successfully proccesed")

        # bye
        return items

