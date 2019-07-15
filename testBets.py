import random

def runBets(sumMoney,numBetsInOneDay,numOfMaxBets):
    day = 0
    while(True):
        day+=1
        maxNumOfLoseBets=0
        for i in range(numBetsInOneDay):
            if(maxNumOfLoseBets!=numOfMaxBets):
                loseOrWin= int(random.uniform(0, 2))
                WIN=1
                if (loseOrWin==WIN):
                    sumMoney +=sumMoney/(2**numOfMaxBets)
                    maxNumOfLoseBets=0
                    if(sumMoney>=1000000):
                        return sumMoney,day
                else:
                    maxNumOfLoseBets+=1
            else:
                return sumMoney,day

numberOfattempts=1
while(True):
    maxWin=runBets(30000,10,10)
    if (maxWin[0]>=1000000):
        print(maxWin)
        print(numberOfattempts)
        numberOfattempts=1
    else:
        numberOfattempts+=1
    
    

