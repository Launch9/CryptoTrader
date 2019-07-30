
class ConfigData:

    isActive = False
    sleepTimeMinutes = 60 * 10

    def __init__(self):
        print("Creating config file...")

    def printSelf(self):
        print("SleepTimeMinutes: " + str(self.sleepTimeMinutes))
        print("IsActive: " + str(self.isActive))