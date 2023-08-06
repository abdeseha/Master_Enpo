import pandas as pd
import matplotlib.pyplot as plt

from calculate import *
from ploting import *

counter = 0
row = 10000
skiprow = 1000
marge = 20
Operations = {}

# rd = input('Read new file (Y/N): ').upper()
# if  rd == 'Y' or rd == 'YES':
#     data = pd.read_excel(input('Data file: '))
#     data.to_csv(r"./data/data.csv")

while True:
    data = pd.read_csv("./data/data.csv", nrows=row, skiprows=skiprow*counter)
    if len(data) < row:
        counter -= 1
        data = pd.read_csv("./data/data.csv", nrows=row, skiprows=skiprow*counter)
    
    P = Calculate.pow(data.iloc[:,1],data.iloc[:,2],data.iloc[:,3])
    P_mavg = Calculate.mob_avg(P,num_vals=20,times=5)
    P_mavg_div = Calculate.div(data.iloc[:,0], P_mavg)
    graph = plot(data.iloc[:,0], Preassure = P, P_avg=P_mavg)

    Characterize.characterize(time=data.iloc[:,0], org_values=P_mavg, dives=P_mavg_div)
    for key, value in Characterize.operations.items():
        print(F'{key} :')
        for key_1, value_1 in value.items():
            print(F'----> {key_1} : {value_1}')
    
    graph.plt_graph()
    graph.shade(Characterize.operations)
    
    counter += 1

plt.show()