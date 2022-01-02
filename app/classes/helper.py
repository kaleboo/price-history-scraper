# modules
import json
import csv
import os

# classes
class Helper:

    def isRunning(filename):
        return os.path.isfile(filename)

    def runningFlag(filename):
        open(filename, 'a').close()

    def removeRunningFlag(filename):
        os.remove(filename)

    def formatNumber(number, decimals = 2):
        return round(float(number), decimals)


    def getVolatility(high1, low1, high2, low2):

        # clean
        high1 = Helper.formatNumber(high1, 8)
        low1 = Helper.formatNumber(low1, 8)
        high2 = Helper.formatNumber(high2, 8)
        low2 = Helper.formatNumber(low2, 8)
        
        # picking the highest value
        high = high1
        
        if (high2 > high):
            high = high2

        # picking the lowest value
        low = low1

        if (low2 < low):
            low = low2

        # bye
        volatility = ((high / low) - 1) * 100

        return Helper.formatNumber(volatility)

    def getTier(volume):

        # volume in U$D

        if volume > 50000000:
            return 1
        elif volume > 10000000:
            return 2
        elif volume > 3000000:
            return 3
        elif volume > 1000000:
            return 4
        else:
            return 5

    def isValidInterval(interval):

        # allowed intervals
        allowed = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d']

        return (interval in allowed)

    def intervalToSeconds(interval):

        # en que unidad está?
        isMins = interval.endswith('m')
        isHours = interval.endswith('h')
        isDays = interval.endswith('d')

        # remover el ultimo char
        number = int(interval.rstrip(interval[-1]))

        # append seconds
        if isMins:
            return number * 60
        elif isHours:
            return number * 3600
        else:
            return number * 86400


    def writeJson(items, filename = "data.json"):
        with open(filename, 'w') as f:
            json.dump(items, f)


    def writeCSV(items, filename = "data.csv"):

        count = 0

        with open(filename, 'w') as f:

            # create the csv writer object
            writer = csv.writer(f)

            for item in items:
                if count == 0:
             
                    # Writing headers of CSV file
                    header = item.keys()
                    writer.writerow(header)
                    count = count + 1
             
                # Writing data of CSV file
                writer.writerow(item.values())
            


