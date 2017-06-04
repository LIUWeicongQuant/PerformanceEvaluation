# Main function to analyze the performance of my stock trading
from WindPy import w
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def ComputeCumuReturn(netValue):
    return netValue[-1]/netValue[0]-1

def ComputeSharpeRatio(netValue):
    # Parameters
    sharpeRatio = 0
    
    # Compute Sharpe ratio
    if len(netValue) > 1:
       retSeq = np.log(netValue[1:] / netValue[:-1])
       sharpeRatio = np.mean(retSeq)*244/(np.std(retSeq)*np.sqrt(244))
    
    # Return values
    return sharpeRatio
    
def ComputeMaxDrawdown(netValue):
    # Parameters
    maxDD = 0
    
    # Compute maximum drawdown
    maxDDSeq = np.zeros([len(netValue), 1])
    for i in range(1, len(netValue)):
        temp = netValue[:i]
        maxDDSeq[i-1] = 1 - temp[-1]/np.max(temp)
    
    maxDD = np.max(maxDDSeq)
    return maxDD
    
def ComputeStats(netValue):
    # Compute stats
    cumuReturn = ComputeCumuReturn(netValue)
    maxDD = ComputeMaxDrawdown(netValue)
    calmar = cumuReturn/maxDD
    sharpeRatio = ComputeSharpeRatio(netValue)
    return list([cumuReturn, maxDD, calmar, sharpeRatio])
    
if __name__ == '__main__':
    ######## Preprocessing ########
    # Parameters
    fileName1 = 'PnL_1.csv'
    fileName2 = 'PnL_2.csv'
    
    # Read the data from the files
    data1 = pd.read_csv(fileName1)
    data2 = pd.read_csv(fileName2)
    
    # link two dataframes
    startDate = str(data1.date[0])
    lastDate = str(data2.date[len(data2)-1])
    
    ######## Get ZZ800 from Wind ########
    # Get the data
    w.start()
    dataStruct = w.wsd('000905.SH', 'close', startDate, lastDate)
    temp = np.array(dataStruct.Data)
    indexData = temp[0]
    indexStats = ComputeStats(indexData)
    print 'Return MaxDD Calmar Sharpe'
    print '%.4f %.4f %.4f %.4f' % tuple(indexStats)
    
    ######## Get the net value of the strategy ########
    # Concatenate two net value sequences
    netValue1 = np.array(data1.net_value)
    netValue2 = np.array(data2.net_value)
    netValue = np.zeros(len(netValue1)+len(netValue2))
    netValue[:len(netValue1)] = netValue1
    for i in range(0, len(netValue2)):
        if i == 0:
            netValue[len(netValue1)] = netValue[len(netValue1)-1]
        else:
            netValue[len(netValue1)+i] = netValue[len(netValue1)+i-1]*(netValue2[i]/netValue2[i-1])
   
    # Compute strategy stats
    strategyStats = ComputeStats(netValue)
    print '%.4f %.4f %.4f %.4f' % tuple(strategyStats)
    
    ######## Plot figures ########
    titleStr1 = 'Net value ' + startDate + ' to ' + lastDate
    titleStr2 = 'ZZ500 ' + startDate + ' to ' + lastDate
    plt.figure(1)
    plt.subplot(2, 1, 1)
    plt.plot(netValue)
    plt.title(titleStr1)
    plt.xlabel('Day')
    plt.ylabel('Net value')
    plt.grid(axis = u'both')
    plt.subplot(2, 1, 2)
    plt.plot(indexData)
    plt.title(titleStr2)
    plt.xlabel('Day')
    plt.ylabel('Index')    