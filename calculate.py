import numpy as np

class Calculate:
    def pow(I_1, I_2, I_3, V=None):
        if V is None:
            V = 400
        power = (I_1 + I_2 + I_3) * V
        return power
    
    def mob_avg(list_in=None, num_vals=1, times=1):
        avrgs = np.empty((0))
        for _ in range(times):
            if len(avrgs) == 0:
                i = 0
                while len(list_in) >= num_vals + i:
                    avrgs = np.append(avrgs, [np.average(list_in[i:num_vals + i])], axis=0)
                    i += 1
            else:
                i = 0
                list_in = avrgs
                avrgs = np.empty((0))
                while len(list_in) >= num_vals + i:
                    avrgs = np.append(avrgs, [np.average(list_in[i:num_vals + i])], axis=0)
                    i += 1
        return avrgs

    def div(time, vals):
        shift = abs(len(time) - len(vals))
        divs = np.empty((0))
        for i in range(1,len(vals)):
            divs = np.append(divs, [(vals[i] - vals[i-1])/(time[i+shift] - time[i+shift -1])], axis=0)
        return divs
    
class Characterize:
    last_time = 0
    operations = {}
    operation = {'nb_of_use':1, 'stab_value':0, 'start_time':np.array([0]), 'end_time':np.array([0]), 'max':np.array([0])}
    operation_num = 1
    in_opt = False
    
    def add_operation():
        if len(Characterize.operations) == 0:
            Characterize.operations[F'operation_{Characterize.operation_num}'] = Characterize.operation
        else:
            for opt in Characterize.operations.values():
                if abs(Characterize.operation['stab_value'] - opt['stab_value']) < Characterize.operation['stab_value']*0.03:
                    opt['nb_of_use'] += 1
                    opt['start_time'] = np.append(opt['start_time'], Characterize.operation['start_time'])
                    opt['end_time'] = np.append(opt['end_time'], Characterize.operation['end_time'])
                    opt['max'] = np.append(opt['max'], Characterize.operation['max'])
                
                else:
                    Characterize.operations[F'operation_{Characterize.operation_num}'] = Characterize.operation
                    Characterize.operation_num += 1

    def characterize(time=None, org_values=None, meaned_values=None, dives=None):
        
        if meaned_values is None :
            meaned_values = org_values

        stab_value = np.empty((0))
        shift_time = len(time)-len(dives)
        shift_org = len(org_values)-len(dives)
        shift_meaned = len(meaned_values)-len(dives)

        for i,dive in enumerate(dives):
            if  time[shift_time+i] >= Characterize.last_time:
                if org_values[shift_org+i] > Characterize.operation['max'][0]:
                    Characterize.operation['max'][0] = org_values[shift_org+i]

                if dive > 5 and Characterize.in_opt == False:
                    Characterize.operation['start_time'][0] = time[shift_time+i]
                    Characterize.in_opt = True
                    
                elif abs(dive) < 5 and meaned_values[shift_meaned+i] > 1000  and  Characterize.in_opt == True:
                    stab_value = np.append(stab_value, [meaned_values[shift_meaned+i]])
                    stab_value = np.array([np.average(stab_value)])
                    Characterize.operation['stab_value'] = stab_value[0]

                elif abs(dive) < 5 and meaned_values[shift_meaned+i] < 100 and Characterize.in_opt == True:
                    Characterize.operation['end_time'] = time[shift_time+i]
                    Characterize.add_operation()
                    Characterize.operation =  {'nb_of_use':1, 'stab_value':0, 'start_time':np.array([0]), 'end_time':np.array([0]), 'max':np.array([0])}
                    Characterize.in_opt = False                    
                     
        Characterize.last_time = time.iloc[-1]