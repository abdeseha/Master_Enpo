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

        avrgs = np.array([])
        i = 0
        
        while self.list_in[0, i:self.range]:
            np.append(avrgs, np.average(self.list_in[0, i:self.range]))
            i += 1
        return avrgs