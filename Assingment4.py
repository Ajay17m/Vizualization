import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats



file = open("TempDump-Indore.txt","r") 
Tempdata=[]
innerdata=[]
i=0
j=0
for line in file: 
    #print('i:',i,'j:',j)
    if i>13:
        innerdata.append(line)
        Tempdata.append(innerdata)
        innerdata=[]
        i=0
    else:
        innerdata.append(line)
        i=i+1
    j=j+1
Tempdata.append(innerdata)
file.close()




Temp=[]
for data in Tempdata:
    Temp.append(data[:9])
TempDF=pd.DataFrame(Temp)
TempDF=TempDF[[2,4]]
TempDF=TempDF.applymap(lambda x: x.replace('\n','').replace('Â°',''))
TempDF['Day']=TempDF[2].apply(lambda x: x.split('/')[1].strip())
TempDF['AvgTemp']=TempDF[4].apply(lambda x: (int(x.split('/')[0].strip())+int(x.split('/')[1].strip()))/2)
TempDF.drop([2,4],axis=1,inplace=True)
TempDF.set_index('Day')
#TempDF.plot()

NSAIL=pd.read_csv('NATNLSTEEL.NS.csv')
NSAIL=NSAIL.set_index(pd.to_datetime(NSAIL['Date']).dt.day)['Close']

MergedData=pd.merge(TempDF,NSAIL,left_index=True,right_index=True,how='left')
MergedData=MergedData.set_index(['Day'])
curr=0
for i in range(30,-1,-1):
    if not(np.isnan(MergedData.iloc[i,1])):
        curr=MergedData.iloc[i,1]
    else:
        MergedData.iloc[i,1]=curr
    #print(MergedData.iloc[i,1])

plt.scatter(MergedData['AvgTemp'],MergedData['Close'])
corr,p_value_corr = stats.spearmanr(MergedData['AvgTemp'],MergedData['Close'])
t_test,p_value_ttest = stats.ttest_rel(MergedData['AvgTemp'],MergedData['Close'])

fig, ax1 = plt.subplots()
color = 'tab:blue'
ax1.set_xlabel('Day of December 2019')
ax1.set_ylabel('Daily average temperature', color=color)
ax1.set_xlim([-1,31])
ax1.set_ylim([0,25])
ax1.plot(MergedData['AvgTemp'], color=color,alpha=0.5,linewidth=2,marker='o')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:red'
ax2.set_ylabel('Daily close price(NATNSTEEL.NS)', color=color)  # we already handled the x-label with ax1
ax2.set_ylim([0,2.5])
ax2.plot(MergedData['Close'], color=color,alpha=0.5,linewidth=2,marker='o')
ax2.tick_params(axis='y', labelcolor=color)
ax1.text(20, 2, 'Correlation cofficient:  {}  p-value :{}\nT-test score              :{}  p-value :{}'.format(
        round(corr,2),round(p_value_corr,2)
        ,round(t_test,2),round(p_value_ttest,2))
        ,style='italic',bbox={'facecolor': 'grey', 'alpha': 0.25, 'pad': 10})

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.gca().set_title('Effect of temprature on stock prices of National Steel & Agro Industries Ltd(NATNLSTEEL.NS)')
plt.show()

