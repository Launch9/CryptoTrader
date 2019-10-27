import json
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np    
import matplotlib.lines as mlines
def newline(p1, p2, lineColor):
    ax = plt.gca()
    xmin, xmax = ax.get_xbound()

    if(p2[0] == p1[0]):
        xmin = xmax = p1[0]
        ymin, ymax = ax.get_ybound()
    else:
        ymax = p1[1]+(p2[1]-p1[1])/(p2[0]-p1[0])*(xmax-p1[0])
        ymin = p1[1]+(p2[1]-p1[1])/(p2[0]-p1[0])*(xmin-p1[0])

    l = mlines.Line2D([xmin,xmax], [ymin,ymax], color=lineColor, linestyle='--')
    ax.add_line(l)
   
    return l

def findY(slope, intercept, xVal):
    return (slope * xVal) + intercept

def makeLine(slope, intercept, xVal1, xVal2, color):
    point1Y = findY(slope, intercept, xVal1)
    point2Y = findY(slope, intercept, xVal2)
    newline([xVal1, point1Y], [xVal2, point2Y], color)

def abline(slope, intercept, lineColor):
    """Plot a line from slope and intercept"""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, '--', color = lineColor)

def lineOfBestFit(points, xLabel, yLabel):
    xSum = 0
    ySum = 0
    for i in points:
        xSum += i[xLabel]
        ySum += i[yLabel]
        plt.scatter(i[xLabel], i[yLabel])
    
    xAverage = xSum / len(points)
    yAverage = ySum / len(points)

    topSummation = 0
    bottomSummation = 0

    for i in points:
        topSummation = (i[xLabel] - xAverage) * (i[yLabel] - yAverage)
        bottomSummation = (i[xLabel] - xAverage)**2

    m = topSummation / bottomSummation
    yIntercept = yAverage - (m*xAverage)
    return {'slope':m, 'y-intercept':yIntercept}

def isPointAbove(x,y, slope, yIntercept):
    value = (slope * x) + yIntercept
    if(y > value):
        return True
    else:
        return False

def findNops(points, slope, yIntercept, xLabel, yLabel):
    isOnSecond = False
    nops = 0
    isAbove = isPointAbove(points[0][xLabel], points[0][yLabel], slope, yIntercept)
    for i in points:
        isCurrentlyAbove = isPointAbove(i[xLabel], i[yLabel], slope, yIntercept)
        if(isCurrentlyAbove != isAbove):
            isAbove = isCurrentlyAbove
            if(isOnSecond):
                nops += 1
                isOnSecond = False
            else:
                isOnSecond = True
    return nops            


def splitXandY(points, xLabel, yLabel):
    xArray = []
    yArray = []
    for i in points:
        xArray.append(i[xLabel])
        yArray.append(i[yLabel])
    return {'x':xArray, 'y': yArray}

def compressLine(points, slope, yIntercept):
    startingDistance = 2000
    howManyLoops = 200
    topLineNops = {'nops': 0, 'y-intercept': 0, 'distanceFromAverage': startingDistance}
    bottomLineNops = {'nops': 0, 'y-intercept': 0, 'distanceFromAverage': startingDistance}
    
    for i in range(howManyLoops):
        #topLine
        yInter = (yIntercept + startingDistance) - (startingDistance * (i/howManyLoops))
        nops = findNops(points, slope, yInter, 'TM', 'C')
        if(nops > topLineNops['nops']):
            topLineNops['nops'] = nops
            topLineNops['y-intercept'] = yInter
            #abline(LBF['slope'], topLineNops['y-intercept'], 'black')
        
        #bottomLine
        yInter = (yIntercept - startingDistance) + (startingDistance * (i/howManyLoops))
        nops = findNops(points, slope, yInter, 'TM', 'C')
        if(nops > bottomLineNops['nops']):
            bottomLineNops['nops'] = nops
            bottomLineNops['y-intercept'] = yInter
            #abline(LBF['slope'], bottomLineNops['y-intercept'], 'yellow')

    profitNops = 0
    hasBought = False
    for i in points:
        
        pointPosition = 0
        if isPointAbove(i['TM'], i['C'], slope, bottomLineNops['y-intercept']):
            if isPointAbove(i['TM'], i['C'], slope, yIntercept):
                if isPointAbove(i['TM'], i['C'], slope, topLineNops['y-intercept']):
                    pointPosition = 2
                else:
                    pointPosition = 1
            else:
                pointPosition = 0
        else:
            pointPosition = -1

        if(pointPosition == -1):
            hasBought = True
        elif(pointPosition == 2):
            if(hasBought):
                profitNops += 1
                hasBought = False
    futurePointTop = findY(slope, topLineNops['y-intercept'], points[-1]['TM'] + 1)
    futurePointBottom = findY(slope, bottomLineNops['y-intercept'], points[-1]['TM'] + 1)
    distanceBetween = futurePointTop - futurePointBottom
    percentIncrease = (distanceBetween / futurePointBottom) * 100
    return {'top': topLineNops, 'bottom': bottomLineNops, 'data': {'distanceBetween': distanceBetween, 'percent': percentIncrease, 'profitNops': profitNops}}


def getBuyandSell(candles, xLabel, yLabel):
    LBF = lineOfBestFit(candles, xLabel, yLabel)
    #print(LBF)

    #print(findNops(candles, LBF['slope'], LBF['y-intercept'], xLabel, yLabel))

    CL = compressLine(candles, LBF['slope'], LBF['y-intercept'])
    #print(CL)

    sellAt = findY(LBF['slope'], CL['top']['y-intercept'], candles[-1][xLabel] + 1)
    buyAt = findY(LBF['slope'], CL['bottom']['y-intercept'], candles[-1][xLabel] + 1)
    return {'sell': sellAt, 'buy': buyAt}


candles = []

"""with open("./USDT-ETH.json") as json_file:
    candles = json.load(json_file)
    for i in candles:
        
        i['O'] = float(i['O'])
        i['H'] = float(i['H'])
        i['L'] = float(i['L'])
        i['C'] = float(i['C'])
        i['V'] = float(i['V'])
        i['BV'] = float(i['BV'])
        
        date_object = datetime.strptime(i['T'], '%Y-%m-%dT%H:%M:%S')
        i['TM'] = int(date_object.strftime("%s")) / 86400
        #date = i['T']
        #newString = ""
        #for b in date:
        #    if(b == 'T'):
        #        break
        #    else:
        #        newString += b
        #i['T'] = newString
    
    json_file.close()

with open("./USDT-ETH.json", 'w') as json_file:
    json.dump(candles, json_file)
    json_file.close()"""

with open("./USDT-ETH.json") as json_file:
    candles = json.load(json_file)

whatWeKnow = candles[0:10]
for i in range(10, len(candles)):
    whatWeKnow.append(candles[i])
    bsData = getBuyandSell(whatWeKnow[-5:], 'TM', 'C')
    print(bsData)
    

coordinateData = splitXandY(candles, 'TM', 'C')
plt.xlabel('Time')
plt.ylabel('Close')
plt.plot(coordinateData['x'], coordinateData['y'], scalex=True)
currentTime = candles[-1]['TM']
makeLine(LBF['slope'], LBF['y-intercept'], currentTime - 5, currentTime + 15, 'blue')
makeLine(LBF['slope'], CL['top']['y-intercept'], currentTime - 5, currentTime + 15, 'green')
makeLine(LBF['slope'], CL['bottom']['y-intercept'], currentTime - 5, currentTime + 15, 'red')

plt.show()

