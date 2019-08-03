from Parser import Parser
from FileReader import FileReader
from StatsGiver import StatsGiver
from FileWriter import FileWriter


class Trader:
    market = {}

    @staticmethod
    def update(self):
        self.market = StatsGiver.get_market_summaries()

    @staticmethod
    def buy(trade_string, how_much_spent):

        # Separating currencies into two different strings
        data = Parser.separateTradeString(trade_string)
        c_one = data['first']
        c_two = data['second']

        # Getting the wallet
        wallet = FileReader.get_wallet()

        summary = StatsGiver.get_market_summary(trade_string)

        # Best price you can get for the trade
        ask_price = summary[0]['Ask']

        # Calculating how much to subtract and add from wallet
        how_much_spent = how_much_spent
        how_much_gained = how_much_spent / ask_price

        print(how_much_spent)
        print(how_much_gained)
        # Storing this transaction
        FileWriter.record_trans(trade_string, True, how_much_spent, how_much_gained, ask_price)

        # Changing values in the wallet
        wallet[c_one] -= how_much_spent  # BTC
        wallet[c_two] += how_much_gained  # LTC

        # Updating the wallet
        FileReader.update_wallet(wallet)

    @staticmethod
    def sell(trade_string, how_much_sold):
        # Separating currencies into two different strings
        data = Parser.separateTradeString(trade_string)
        c_one = data['first']
        c_two = data['second']

        # Getting the wallet
        wallet = FileReader.get_wallet()

        summary = StatsGiver.get_market_summary(trade_string)

        # Best price you can get for the trade
        bid_price = summary[0]['Bid']

        # Calculating how much to subtract and add from wallet
        how_much_gained = how_much_sold / bid_price

        print(how_much_sold)
        print(how_much_gained)
        # Storing this transaction
        FileWriter.record_trans(trade_string, False, how_much_sold, how_much_gained, bid_price)

        # Changing values in the wallet
        wallet[c_one] += how_much_gained  # BTC
        wallet[c_two] -= how_much_sold  # LTC

        # Updating the wallet
        FileReader.update_wallet(wallet)
