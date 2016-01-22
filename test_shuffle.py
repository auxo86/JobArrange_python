import random
testList = [i for i in range(0,100,1)]
sumTimes = [0 for i in range(0,100,1)]
x=100000/100
for i in range(0,100000,1):
    random.shuffle(testList)
    sumTimes[testList.index(1)]+=1

for i in range(0,100,1):
    sumTimes[i] /= x
    sumTimes[i]= str(sumTimes[i]) + '%'
print('平均次數應為 ',x ,' 次')
print('次數機率陣列:',sumTimes)
