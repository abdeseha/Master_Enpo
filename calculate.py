import numpy as np

class Calculate:
    def pow(I_1, I_2, I_3, V=None):
        if V is None:
            V = 400
        power = (I_1 + I_2 + I_3) * V
        return power

    def mob_avg(list_in=None, num_vals=1, times=1):
        avrgs = np.empty((0))
        confs = np.empty((0))

        for i in range(1,num_vals+1):
            confs = np.append(confs, [i**5])

        for _ in range(times):
            if len(avrgs) == 0:
                i = 0
                while len(list_in) >= num_vals + i:
                    avrgs = np.append(avrgs, [np.sum(list_in[i:num_vals + i]*confs) / np.sum(confs)], axis=0)
                    i += 1
            else:
                i = 0
                list_in = avrgs
                avrgs = np.empty((0))
                while len(list_in) >= num_vals + i:
                    avrgs = np.append(avrgs, [np.sum(list_in[i:num_vals + i]*confs) / np.sum(confs)], axis=0)
                    i += 1
        return avrgs

    def div(time=None, vals=None):
        shift = abs(len(time) - len(vals))
        divs = np.empty((0))
        for i in range(1,len(vals)):
            divs = np.append(divs, [(vals[i] - vals[i-1])/(time[i+shift] - time[i+shift -1])], axis=0)
        return divs
    
class Characterize:

    def __init__(self, operations={}, temp_opts={}, in_opt=False, last_time=0, operations_num=1, dump_opts=[], stat = ""):
        self.operations = operations
        self.last_time = last_time
        self.operations_num = operations_num
        self.operation = temp_opts
        self.in_opt = in_opt
        self.dump_opts = dump_opts
        self.stat = stat

    def add_operation(self):
        in_opts = False
        if len(self.operations) == 0:
            self.operations[F'operation_{self.operations_num}'] = self.operation
        else:
            for opt in self.operations.values():
                if abs(self.operation['stab_value'] - opt['stab_value']) < self.operation['stab_value']*0.03:
                    in_opts = True
                    opt['nb_of_use'] += 1
                    opt['start_time'] = np.append(opt['start_time'], self.operation['start_time'])
                    opt['end_time'] = np.append(opt['end_time'], self.operation['end_time'])
                    opt['max'] = np.append(opt['max'], self.operation['max'])
            if in_opts == False:
                self.operations_num += 1
                self.operations[F'operation_{self.operations_num}'] = self.operation
        return

    def characterize(self, time=None, org_values=None, meaned_values=None, dives=None):
        shift_time = len(time)-len(dives)
        shift_org = len(org_values)-len(dives)
        shift_meaned = len(meaned_values)-len(dives)
        dump_in_op = self.in_opt

        for i,dive in enumerate(dives):
            if  time[shift_time+i] >= self.last_time:
                if org_values[shift_org+i] > self.operation['max'][0]:
                    self.operation['max'][0] = org_values[shift_org+i]

                if dive > 5 and self.in_opt == False:
                    self.operation['start_time'][0] = time[shift_time+i]
                    self.in_opt = True
                    
                elif abs(dive) < 5 and meaned_values[shift_meaned+i] > 1000  and  self.in_opt == True:
                    self.operation['stab_value'] = np.append(self.operation['stab_value'], [meaned_values[shift_meaned+i]])

                elif abs(dive) < 5 and meaned_values[shift_meaned+i] < 100 and self.in_opt == True:
                    self.operation['end_time'][0] = time[shift_time+i]
                    self.operation['stab_value'] = np.array([np.average(self.operation['stab_value'])])[0]
                    Characterize.add_operation(self)
                    self.operation =  {'nb_of_use':1,
                                        'stab_value':0,
                                        'start_time':np.array([0]), 
                                        'end_time':np.array([0]),
                                        'max':np.array([0])}
                    self.in_opt = False
        
        self.dump_charact(time, meaned_values, dives, dump_in_op)                    
        self.last_time = time.iloc[-1]

        return self.operations ,self.operation, self.in_opt, self.last_time, self.operations_num, self.dump_opts, self.stat
    
    def dump_charact(self,time=None, meaned_values=None , dives=None, dump_in_opt=False):
        shift_time = len(time)-len(dives)
        shift_meaned = len(meaned_values)-len(dives)

        for i,dive in enumerate(dives):
            if  time[shift_time+i] >= self.last_time:

                if dive > 5 and dump_in_opt == False:
                    dump_in_opt = True
                    self.dump_opts.append({})
                    
                if abs(dive) < 5 and meaned_values[shift_meaned+i] < 100 and dump_in_opt == True:
                    dump_in_opt = False
                    self.dump_opts[-1][time[shift_time+i]] = meaned_values[shift_meaned+i]

                if dump_in_opt == True:        
                    if abs(dive) <= 20 and self.stat != 'stable':
                        self.stat = 'stable'
                        self.dump_opts[-1][time[shift_time+i]] = meaned_values[shift_meaned+i]
                    elif dive > 20 and self.stat != 'increase':
                        self.stat = 'increase'
                        self.dump_opts[-1][time[shift_time+i]] = meaned_values[shift_meaned+i]
                    elif dive < -20 and self.stat != 'decrease':
                        self.stat = 'decrease'
                        self.dump_opts[-1][time[shift_time+i]] = meaned_values[shift_meaned+i]
        return