import numpy as np

class calculate:
    def Pow(I_1, I_2, I_3, V=None):
        if V is None:
            V = 400
        power = (I_1 + I_2 + I_3) * V
        return power
    
    def mob_avg(list_in=None,range=1):

        avrgs = np.empty((0))
        i = 0

        while len(list_in) >= range + i:
            avrgs = np.append(avrgs, [np.average(list_in[i:range + i-1])], axis=0)
            i += 1
        return avrgs

    def div(time, vals):
        shift = abs(len(time) - len(vals))
        divs = np.empty((0))
        for i, value in enumerate(vals[1:]):
             divs = np.append(divs, [(value - vals[i-1])/(time[i+shift] - time[i+shift -1])], axis=0)
        return divs
    