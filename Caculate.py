import numpy as np

class Elt_power:
    """Caclulate the electric power"""
    def __init__(self, I_1, I_2, I_3, V=None):
        self.I_1 = I_1
        self.I_2 = I_2
        self.I_3 = I_3
        if V is None:
            V = 400
        self.V = V

    def Pow(self):
        power = (self.I_1 + self.I_2 + self.I_3) * self.V
        return power


class Mavrg:
    """Caculate the Mobile average or a list"""
    def __init__(self,list_in=None,range=1):
        self.list_in = list_in
        self.range = range

    def mob_avg(self):

        avrgs = np.empty((0))
        i = 0

        while (len(self.list_in) - i) >= self.range :
            avrgs = np.append(avrgs, [np.average(self.list_in[i:self.range + i])], axis=0)
            i += 1
        return avrgs
    

class Derive:
    """"Caculate the derivitive"""
    def __init__(self, time, vals):
        self.time = time
        self.vals = vals

    def div(self):
        shift = abs(len(self.time) - len(self.vals))
        divs = np.empty((0))
        for i, value in enumerate(self.vals[1:]):
             divs = np.append(divs, [(value - self.vals[i-1])/(self.time[i+shift] - self.time[i+shift -1])], axis=0)
        return divs
    