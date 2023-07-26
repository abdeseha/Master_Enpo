import pandas as pd
import numpy as np

from caculate import *
from ploting import *

counter = 0

rd = input('Read new file (Y/N): ').upper()
if  rd == 'Y' or rd == 'YES':
    data = pd.read_excel(input('Data file: '))
    data.to_csv(r"data.csv")

while True:
    try:
        data = pd.read_csv("data.csv", nrows=10000, skiprows=100*counter)
    except pd.errors.EmptyDataError:
        counter -= 1
        data = pd.read_csv("data.csv", nrows=10000, skiprows=100*counter)
    finally:
        P = Elt_power(data.iloc[:,1],data.iloc[:,2],data.iloc[:,3]).Pow()
        P_mavg_1 = Mavrg(P,range=20).mob_avg()
        P_mavg_2 = Mavrg(P_mavg_1, range=20).mob_avg()
        P_mavg_2_div = Derive(data.iloc[:,0], P_mavg_2).div()
        print(P_mavg_2_div.shape)
        print(P_mavg_2_div)
    counter += 1