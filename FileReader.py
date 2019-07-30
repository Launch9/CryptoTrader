from ConfigData import ConfigData
import json



class FileReader:

    def __init__(self):
        print("Initializing FileReader.")

    def read_config(self):

        print("Reading config...")
        cd = ConfigData()
        f = open("data/config.txt", "r")

        for line in f:
            cache = ""
            i = 0
            varType = -1
            while i < len(line):

                if line[i] == '=':
                    cache = ''
                    i += 1
                    continue
                cache = cache + line[i]
                if varType == -1:
                    if cache == "SLEEP_TIME_MINUTES":
                        varType = 0

                    elif cache == "IS_ACTIVE":
                        varType = 1
                else:
                    if varType == 0:
                        cd.sleepTimeMinutes = int(cache)
                    elif varType == 1:
                        if cache == "0":
                            cd.isActive = False
                        elif cache == "1":
                            cd.isActive = True

                i += 1

        return cd

    def get_wallet(self):
        with open('data/wallet.json') as json_file:
            return json.load(json_file)

    def update_wallet(self, data):
        with open('data/wallet.json', 'w') as json_file:
            json.dump(data, json_file)
            json_file.close()