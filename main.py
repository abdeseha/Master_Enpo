import pandas as pd
import matplotlib.pyplot as plt

from caculate import *
from ploting import *

counter = 0
row = 10000
skiprow = 1000
marge = 40

rd = input('Read new file (Y/N): ').upper()
if  rd == 'Y' or rd == 'YES':
    data = pd.read_excel(input('Data file: '))
    data.to_csv(r"./data/data.csv")

while True:
    data = pd.read_csv("./data/data.csv", nrows=row, skiprows=skiprow*counter)
    if len(data) < row:
        counter -= 1
        data = pd.read_csv("./data/data.csv", nrows=row, skiprows=skiprow*counter)
    
    P = calculate.Pow(data.iloc[:,1],data.iloc[:,2],data.iloc[:,3])
    P_mavg_1 = calculate.mob_avg(P,range=marge)
    P_mavg_2 = calculate.mob_avg(P_mavg_1, range=marge)
    P_mavg_2_div = calculate.div(data.iloc[:,0], P_mavg_2)
    graph = plot(data.iloc[:,0], prussur = P)
    graph.set_anime()
    counter += 1

plt.show()