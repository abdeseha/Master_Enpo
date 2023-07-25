import pandas as pd
import numpy as np

from Caculate import *
from ploting import *
if input('Read new file (Y/N): ').upper == 'Y' or 'YES':
    data = pd.read_excel(input('Data file: '))
    data.to_csv(r"data.csv", index= None, header=True)

data = pd.read_csv("data.csv", nrows=10000, skiprows=0)

print(data)