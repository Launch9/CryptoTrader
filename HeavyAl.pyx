print("I got called!")

def HeavyAl(trade_string, interval, candles):
    stat_sum = 0
    number_of_passes = 0

    for i in candles:
        mid_average = ((float(i['open']) + float(i['close'])) / 2)
        stat_sum += mid_average
    average = stat_sum / len(candles)
    for i in candles:
        open_v = float(i['open'])
        close_v = float(i['close'])
        if ((average <= open_v) & (average >= close_v)) | ((average >= open_v) & (average <= close_v)):
            number_of_passes += 1

    return {'marketName': trade_string, 'average': average, "nop": number_of_passes}