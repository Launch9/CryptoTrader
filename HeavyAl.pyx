
#cython: binding=True, boundscheck=True, wraparound=True, nonecheck=True

def find_passes(candles, line):
    cdef double close_v = 0
    cdef double open_v = 0
    cdef int number_of_passes = 0
    for i in candles:
        open_v = <double>float(i['open'])
        close_v = <double>float(i['close'])
        if ((line <= open_v) & (line >= close_v)) | ((line >= open_v) & (line <= close_v)):
            number_of_passes += 1
    return number_of_passes


def algo1(str trade_string, str interval, candles):


        cdef double stat_sum = 0
        cdef int number_of_passes = 0
        cdef double mid_average = 0
        
        for i in candles:
            mid_average = ((<double>float(i['open']) + <double>float(i['close'])) / 2.0)
            stat_sum += mid_average
        cdef double average = stat_sum / len(candles)
        cdef int nop_average = find_passes(candles, average)
        scrunch_data = []
        cdef double block_size = (average * 0.80)
        cdef double buy_line = 0
        cdef double sell_line = 0
        cdef int buy_nop = 0
        cdef int sell_nop = 0
        cdef int opti_num = 100
        
        #Shrinking sell_line
        for i in range(opti_num):
            sell_line = average + (block_size / (i + 1))
            b = find_passes(candles, sell_line)
            scrunch_data.append(b)
            if b > sell_nop:
                sell_nop = b
        for i in range(opti_num):
            if sell_nop == scrunch_data[i]:
                sell_line = average + (block_size / (i + 1))

        #Resetting variables
        scrunch_data = []

        #Shrinking buy_line
        for i in range(opti_num):
            buy_line = average - (block_size / (i + 1))
            b = find_passes(candles, buy_line)
            scrunch_data.append(b)
            if b > buy_nop:
                buy_nop = b
        for i in range(opti_num):
            if buy_nop == scrunch_data[i]:
                buy_line = average - (block_size / (i + 1))

        cdef double percent_increase = ((sell_line - buy_line) / buy_line) * 100
        cdef int current_pos = 0
        cdef double current = <double>float(candles[len(candles) - 1]['close'])

        #Calculating the current position. Helps in determining if the trade is worth investing in right now.
        if(current > sell_line):
            current_pos = 2

        if(current > mid_average and current < sell_line):
            current_pos = 1
        
        if(current < mid_average and current > buy_line):
            current_pos = -1

        if(current < buy_line):
            current_pos = -2
        
        
        
        return {'marketName': trade_string, 
        'average': average,
        'buy': buy_line,
        'sell': sell_line,
        "nop-average": number_of_passes,
        'nop-buy': buy_nop,
        'nop-sell': sell_nop,
        'percent': percent_increase,
        "currentPos": current_pos
        }
