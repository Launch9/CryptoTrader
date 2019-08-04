class Parser:

    @staticmethod
    def findCurrency(currentStats):
        print(currentStats[0])
        return currentStats[0]

    @staticmethod
    def separateTradeString(tradeString):
        first_currency = ""
        second_currency = ""
        is_on_first = True
        for x in tradeString:
            if x == '-':
                is_on_first = False
                continue

            if is_on_first:
                first_currency = first_currency + x
            else:
                second_currency = second_currency + x

        return {"first": first_currency, "second": second_currency}

    @staticmethod
    def reverse_trade_string(trade_string):
        split = Parser.separateTradeString(trade_string)
        return split['second'] + '-' + split['first']

    @staticmethod
    def find_market_strings(main_coin, market):
        re = []
        for obj in market:
            if (Parser.separateTradeString(obj['MarketName'])['first'] == main_coin):
                re.append(obj)

        return re

