import pandas as pd
import numpy as np
from calculate import *
import time as temps
import random

class Analyse_C:
    in_loop = False
    on = False
    counters = [0]
    last_times = [0]
    file_opts = {}
    file_dump_ops = {}
    temp_opts =  {}
    file_opts_num = [0]
    in_opts = {}
    stat = [""]

    def __init__(self, files=None, on=True, row=10000, skiprow=1000, marge=20, times=5):
        self.files = files
        self.on = on
        self.row = row
        self.skiprow = skiprow
        self.marge = marge 
        self.times = times

    def Analyse(self,index):
        
        if self.files[index].lower().endswith(".csv"):
            data = pd.read_csv(self.files[index], nrows=self.row, skiprows=self.skiprow*Analyse_C.counters[index])
        else:
            data = pd.read_excel(self.files[index], nrows=self.row, skiprows=self.skiprow*Analyse_C.counters[index])
        
        if len(data) < 2:
            temps.sleep(10)
            return
        elif len(data) < self.row:
            if self.files[index].lower().endswith(".csv"):
                data = pd.read_csv(self.files[index], skiprows=self.skiprow*Analyse_C.counters[index])
            else:
                data = pd.read_excel(self.files[index], skiprows=self.skiprow*Analyse_C.counters[index])
            Analyse_C.counters[index] -= 1

        try:
            self.P = Calculate.pow(data.iloc[:,1],data.iloc[:,2],data.iloc[:,3],data.iloc[:,4])
        except IndexError:
            self.P = Calculate.pow(data.iloc[:,1],data.iloc[:,2],data.iloc[:,3])
        
        adding = np.full((1,self.marge*self.times - self.times), self.P[0])
        self.P = np.append(adding, self.P)
        self.time = data.iloc[:,0]

        self.P_mavg = Calculate.mob_avg(self.P,self.marge,self.times)
        P_mavg_div = Calculate.div(self.time, self.P_mavg)
        self.P = np.delete(self.P, range(1,self.marge*self.times - self.times+1))
        
        (Analyse_C.file_opts[f"file_{index}"],
        Analyse_C.temp_opts[f"file_{index}"],
        Analyse_C.in_opts[f"file_{index}"],
        Analyse_C.last_times[index],
        Analyse_C.file_opts_num[index],
        Analyse_C.file_dump_ops[f"file_{index}"],
        Analyse_C.stat[index]) = Characterize(Analyse_C.file_opts[f"file_{index}"],
                                                Analyse_C.temp_opts[f"file_{index}"],
                                                Analyse_C.in_opts[f"file_{index}"],
                                                Analyse_C.last_times[index],
                                                Analyse_C.file_opts_num[index],
                                                Analyse_C.file_dump_ops[f"file_{index}"],
                                                Analyse_C.stat[index])\
                .characterize(time=self.time, org_values=self.P, meaned_values=self.P_mavg, dives=P_mavg_div)
        return

    def draw_chart(self, gui, mb_p = False, tot_pow = False):
        colors = []
        lines = []

        for _ in range(len(self.files)):
            color = (random.randint(0, 10)*25/255, random.randint(0, 10)/255, random.randint(0, 10)*25/255)
            while color in colors and color == (0, 0, 0):
                color = (random.randint(0, 10)*25/255, random.randint(0, 10)/255, random.randint(0, 10)*25/255)
            colors.append(color)

        while Analyse_C.on:
            pre_time = None
            Analyse_C.in_loop = True
            gui.figure.clf()
            gui.ax = gui.canvas.figure.add_subplot(111)
            for index in range(len(self.files)):
                try:
                    self.Analyse(index)
                    if index == 0 :
                        if tot_pow: 
                            self.p_tot = np.zeros(len(self.time))
                except TypeError:
                    gui.ax.set_title('There is an error with your data, stop analysing')
                    gui.canvas.draw()
                    return
                if not mb_p :
                    if tot_pow: Analyse_C.Total_power(self, self.P, pre_time)
                    line, = gui.ax.plot(self.time[:len(self.P_mavg)], self.P, color=colors[index])
                    lines.append(line,)
                else:
                    if tot_pow: Analyse_C.Total_power(self, self.P_mavg, pre_time)
                    line, = gui.ax.plot(self.time[:len(self.P_mavg)], self.P_mavg, color=colors[index])
                    lines.append(line,)
                Analyse_C.counters[index] += 1
                pre_time = self.time
                
            
            if tot_pow:
                lin_tot, = gui.ax.plot(self.time, self.p_tot, color='black', linestyle='--')
                lines.append(lin_tot,)
                
            Analyse_C.counters = [min(Analyse_C.counters)]*len(self.files)
            
            splited = []
            for ln in self.files:
                splited.append(ln.split("/")[-1])
            if tot_pow: splited.append('Total Power')

            gui.ax.legend(lines, splited, loc='upper left')
            gui.ax.set_xlabel('Time [s]')
            gui.ax.set_ylabel('Electric Power [W]')
            gui.canvas.draw()
            lines = []
            Analyse_C.in_loop = False
        return

    def Total_power(self, p, pre_time):
        if len(self.p_tot) >= len(p):
            for i in range(len(p)):
                try:
                    self.p_tot[i] += p[i]
                except IndexError:
                    self.p_tot[i] += 0
            if pre_time is not None:
                self.time = pre_time

        else:
            for i in range(len(p)):
                try:
                    self.p_tot[i] += p[i]
                except IndexError:
                    self.p_tot = np.append(self.p_tot, p[i])

        return
    
    def new(n_files):
        if not Analyse_C.on:
            Analyse_C.counters = [0]*n_files
            Analyse_C.last_times = [0]*n_files
            Analyse_C.file_opts_num = [1]*n_files
            Analyse_C.stat = [""]*n_files
            Analyse_C.file_opts = {}
            Analyse_C.file_dump_ops = {}
            Analyse_C.temp_opts = {}
            for i in range(n_files):
                Analyse_C.file_opts[f'file_{i}'] = {}
                Analyse_C.file_dump_ops[f'file_{i}'] = []
                Analyse_C.temp_opts[f'file_{i}'] =\
                    {'nb_of_use':1,
                    'stab_value':0,
                    'start_time':np.array([0]),
                    'end_time':np.array([0]), 
                    'max':np.array([0])}
                Analyse_C.in_opts[f'file_{i}'] = False
        return