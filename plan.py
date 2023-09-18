import sqlite3
from itertools import permutations
from scipy.interpolate import interp1d
import numpy as np

class Plan:
    def __init__(self):
        self.connection = sqlite3.connect('./assets/operataion_list.db')
        self.cursor = self.connection.cursor()

    def add_to_db(self, opt, opt_name):
        if opt != {} and opt_name != '' and opt_name != 'NONE':
            self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS "{opt_name}" (
                Time int,
                Value int
            )                            
            ''')

            for time, value in opt.items():
                self.cursor.execute(f'''
                INSERT INTO "{opt_name}" VALUES
                ({time}, {value})
                ''')
            
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        operations = self.cursor.fetchall()
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        return operations
    
    def rm_opt(self, opt):
        self.cursor.execute(f'DROP TABLE IF EXISTS "{opt}";')
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        return
    
    def schedule(self, table, max_pow, done):
        self.max_pow = max_pow
        types = [i[0] for i in table]
        types_copy = list(types)
        self.best_table = [i[1:] for i in table]
        self.swap = []
        new_table =[]
        self.temp_table = []
        self.opt_list = {}
        self.total_time = []
        self.total_power = []
        self.t_max = 0

        #------------------- Operatoin that has the same type ----------------#
        for type in types:
            self.swap.append([])
            for i in range(len(types)):
                if type == types_copy[i]:
                    self.swap[-1].append(i)
                    types_copy[i] = 'No_type'
            if self.swap[-1] == []:
                self.swap.pop(-1)

        for i in self.swap:
            new_table.append([])
            for j in i:
                for op in table[j][1:]:
                    new_table[-1].append(op)
        
        #----------------------- read data for the use operations ---------------#
        for y in table:
            for x in y[1:]:
                if x not in self.opt_list and x != 'NONE':
                    self.cursor.execute(f"SELECT * FROM '{x}'")
                    points = self.cursor.fetchall()
                    self.opt_list[x] = points

        #--------------------------- check if power is not low -------------------#
        for values in self.opt_list.values():
            for value in values:
                if value[1] > max_pow:
                    self.cursor.close()
                    self.connection.close()
                    done.cr_sched.setEnabled(True)
                    return self.best_table, self.total_time, self.total_power           

        self.cursor.close()
        self.connection.close()

        #--------------------- trying every possibility ------------------------#
        self.temp_table = list(new_table)
        permutation_generator = [Plan.generate_permutations(ls) for ls in new_table]
        Plan.switching(self, new_table, permutation_generator, 0, self.temp_table)

        done.cr_sched.setEnabled(True)
        done.ana.setEnabled(True)
        done.settings.setEnabled(True)
        return self.best_table, self.total_time, self.total_power
    
    def generate_permutations(input_list):
        for perm in permutations(input_list):
            yield perm

    def switching(self, my_list, permutation_generator, i, output_list):
        if i+1 > len(permutation_generator): i=0
        for perm in permutation_generator[i]:
            output_list[i] = perm
            Plan.time_fixing(self, output_list)
            if i+1 == len(permutation_generator):
                continue
            Plan.switching(self, my_list, permutation_generator, i+1, output_list)
        if i != 0:
            permutation_generator[i] = Plan.generate_permutations(my_list[i])

    def time_fixing(self, list_in):
        table = []
        end_time = [0]*len(self.best_table)
        total_power = []
        total_time = []
        for f,opts in enumerate(self.swap):
            number = int(len(list_in[f])/len(opts))
            for r,opt in enumerate(opts):
                start_at = number*r
                up_to = number*(r+1)
                table.insert(opt, list_in[f][start_at: up_to])
        temp_table = []
        for i in range(len(table)):
            temp_table.append([])

        for z,col in enumerate(table):
            if z == 0:
                for opt in col:
                    if opt in self.opt_list:
                        for val in self.opt_list[opt]:
                            total_time.append(val[0]+end_time[z])
                            total_power.append(val[1])
                        end_time[z] += val[0]
                        temp_table[z].append(opt)
                if total_time == []:
                    total_time.append(0)
                    total_power.append(0)    
            else :
                for opt in col:
                    moving = True
                    t_opt=[]
                    p_opt = []
                    start_opt = 0
                    end_opt = 0
                    start_opt_index = 0
                    end_opt_index = 0
                    start_total = 0
                    start_total_index = 0
                    end_total = 0
                    end_total_index = 0
                    total_time_all = []
                    total_power_new = []

                    if opt in self.opt_list:
                        shift = 0
                        while moving:
                            t_opt = []
                            p_opt = []
                            for val in self.opt_list[opt]:
                                t_opt.append(val[0])
                                p_opt.append(val[1])
                            t_opt = [h + end_time[z] for h in t_opt]
                            
                            start_opt = t_opt[0]
                            end_opt = t_opt[-1]
                            start_total = total_time[0]
                            end_total = total_time[-1]

                            interp_total = interp1d(total_time, total_power, kind='linear')
                            interp_opt = interp1d(t_opt, p_opt, kind='linear')
                            
                            total_time_all = total_time + t_opt
                            total_time_all = list(dict.fromkeys(total_time_all))
                            total_time_all.sort()

                            start_opt_index = total_time_all.index(start_opt)
                            end_opt_index = total_time_all.index(end_opt)
                            start_total_index = total_time_all.index(start_total)
                            end_total_index = total_time_all.index(end_total)
                            
                            interpol_total_p = interp_total(total_time_all[start_total_index:end_total_index+1])
                            interpol_opt_p = interp_opt(total_time_all[start_opt_index:end_opt_index+1])

                            for i in range(len(total_time_all)):
                                if i < start_opt_index:
                                    interpol_opt_p = np.insert(interpol_opt_p, 0, 0)
                                elif i > end_opt_index:
                                    interpol_opt_p = np.append(interpol_opt_p, [0])
                            
                                if i < start_total_index:
                                    interpol_total_p = np.insert(interpol_total_p, i, 0)
                                elif i > end_total_index:
                                    interpol_total_p = np.append(interpol_total_p, [0])

                            total_power_new = []
                            total_power_new = [x+y for x,y in zip(interpol_opt_p, interpol_total_p)]
                            p = max(total_power_new)
                            if p >= self.max_pow:
                                shift += 10 
                                end_time[z] += 10
                                total_time_all = list(total_time)
                                total_power_new = list(total_power)
                            else:
                                if shift == 0:
                                    temp_table[z].append(opt)
                                    total_time = list(total_time_all)
                                    total_power = list(total_power_new)
                                    end_time[z] = t_opt[-1]
                                    moving = False
                                else:
                                    temp_table[z].append(f'{shift} (s)')
                                    temp_table[z].append(opt)
                                    total_time = list(total_time_all)
                                    total_power = list(total_power_new)
                                    end_time[z] = t_opt[-1]
                                    moving = False

        if self.t_max == 0 or self.t_max > max(end_time):
            self.t_max = max(end_time)
            self.best_table = list(temp_table)
            self.total_power = list(total_power)
            self.total_time = list(total_time)