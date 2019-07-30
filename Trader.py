from Parser import Parser
from FileReader import FileReader
from StatsGiver import StatsGiver
from FileWriter import FileWriter


class Trader:
    market = {}
    parser = Parser()
    fileWriter = None
    fileReader = None
    statsGiver = None

    def __init__(self, fileReader, fileWriter, statsGiver):
        self.fileReader = fileReader
        self.fileWriter = fileWriter
        self.statsGiver = statsGiver

    def update(self):
        self.market = self.statsGiver.get_market_summaries()

    def buy(self, trade_string, how_much_spent):

        # Separating currencies into two different strings
        data = self.parser.separateTradeString(trade_string)
        c_one = data['first']
        c_two = data['second']

        # Getting the wallet
        wallet = self.fileReader.get_wallet()

        summary = self.statsGiver.get_market_summary(trade_string)

        # Best price you can get for the trade
        ask_price = summary[0]['Ask']

        # Calculating how much to subtract and add from wallet
        how_much_spent = how_much_spent
        how_much_gained = how_much_spent / ask_price

        print(how_much_spent)
        print(how_much_gained)
        # Storing this transaction
        self.fileWriter.record_trans(trade_string, True, how_much_spent, how_much_gained, ask_price)

        # Changing values in the wallet
        wallet[c_one] -= how_much_spent  # BTC
        wallet[c_two] += how_much_gained  # LTC

        # Updating the wallet
        self.fileReader.update_wallet(wallet)

    def sell(self, trade_string, how_much_sold):
        # Separating currencies into two different strings
        data = self.parser.separateTradeString(trade_string)
        c_one = data['first']
        c_two = data['second']

        # Getting the wallet
        wallet = self.fileReader.get_wallet()

        summary = self.statsGiver.get_market_summary(trade_string)

        # Best price you can get for the trade
        bid_price = summary[0]['Bid']

        # Calculating how much to subtract and add from wallet
        how_much_spent = how_much_spent
        how_much_gained = how_much_spent / ask_price

        print(how_much_spent)
        print(how_much_gained)
        # Storing this transaction
        self.fileWriter.record_trans(trade_string, True, how_much_spent, how_much_gained, ask_price)

        # Changing values in the wallet
        wallet[c_one] -= how_much_spent  # BTC
        wallet[c_two] += how_much_gained  # LTC

        # Updating the wallet
        self.fileReader.update_wallet(wallet)
