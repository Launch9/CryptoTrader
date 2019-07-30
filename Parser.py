class Parser:
    def __init__(self):
        print("Initializing Parser.")

    def findCurrency(self, currentStats):
        print(currentStats[0])
        return currentStats[0]

    def separateTradeString(self, tradeString):
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
