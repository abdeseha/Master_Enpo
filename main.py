import pandas as pd
import numpy as np

from caculate import *
from ploting import *

counter = 0

rd = input('Read new file (Y/N): ').upper()
if  rd == 'Y' or rd == 'YES':
    data = pd.read_excel(input('Data file: '), index = True)
    data.to_csv(r"data.csv")

while True:
    data = pd.read_csv("data.csv", nrows=10000, skiprows=10000*counter)
    print(data[0])
    #P = Elt_power(data[])