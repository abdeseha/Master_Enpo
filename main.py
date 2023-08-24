from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QCheckBox 
from PyQt5.QtWidgets import QSpinBox, QVBoxLayout, QFileDialog, QAction
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import uic
import threading
import openpyxl
import matplotlib.pyplot as plt
import sys
from analyse import Analyse_C

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()

        self.files = None

        uic.loadUi("./assets/app_gui.ui", self)

        self.lay = self.findChild(QVBoxLayout, "plot_holder")
        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self.figure)
        self.lay.addWidget(self.canvas)

        self.apply = self.findChild(QPushButton, "apply")
        self.apply.setEnabled(False)
        self.stop = self.findChild(QPushButton, "stop")
        self.stop.setEnabled(False)
        self.chfile = self.findChild(QPushButton, "file")
        self.to_pause = self.findChild(QPushButton, "to_pause")
        self.to_pause.setEnabled(False)
        self.to_continue = self.findChild(QPushButton, "to_continue")
        self.to_continue.setEnabled(False)
        self.mob_pressure = self.findChild(QCheckBox, 'Mob_pressure')
        self.tot_pow = self.findChild(QCheckBox, 'tot_pow')

        self.skip_row_box = self.findChild(QSpinBox, 'skip_row_box')
        self.rows_box = self.findChild(QSpinBox, 'rows_box')
        self.num_vals = self.findChild(QSpinBox, "num_vals")
        self.num_times = self.findChild(QSpinBox, "num_times")

        self.new_file = self.findChild(QAction, "actionNew_File")
        self.to_continue.setEnabled(False)
        self.save_tab = self.findChild(QAction, "actionSave_Table")
        self.save_tab.setEnabled(False)

        app.aboutToQuit.connect(self.stop_app)
        self.apply.clicked.connect(self.start_analyse)
       
        self.stop.clicked.connect(self.stop_analyse)
        self.chfile.clicked.connect(self.choose_file)
        self.to_pause.clicked.connect(self.pausing)
        self.to_continue.clicked.connect(self.continueing)
        self.new_file.triggered.connect(self.creat_new_file)
        self.save_tab.triggered.connect(self.save_opts)
        self.skip_row_box.valueChanged.connect(self.update_min)
        self.show()

    def choose_file(self):
        self.files, _ = QFileDialog.getOpenFileNames(self, "Open File", "", "Excel Files (*.xlsx *.csv)")
        if self.files != []:
            Analyse_C.new(len(self.files))

            self.stop.setEnabled(False)
            self.apply.setEnabled(True)
            self.to_continue.setEnabled(False)
            self.to_pause.setEnabled(False)
    
    def start_analyse(self):
        Analyse_C.on = True

        self.stop.setEnabled(True)
        self.apply.setEnabled(False)
        self.chfile.setEnabled(False)
        self.to_continue.setEnabled(False)
        self.to_pause.setEnabled(True)
        self.skip_row_box.setEnabled(False)
        self.rows_box.setEnabled(False)
        self.num_vals.setEnabled(False)
        self.num_times.setEnabled(False)
        self.save_tab.setEnabled(False)
        self.new_file.setEnabled(False)
        self.mob_pressure.setEnabled(False)
        self.tot_pow.setEnabled(False)
        chart = Analyse_C(files=self.files,
                          row=self.rows_box.value(), skiprow=self.skip_row_box.value(),
                          marge=self.num_vals.value(), times=self.num_times.value(),
                          )
        self.analyse_thread = threading.Thread(target=chart.draw_chart, args = (self, self.mob_pressure.isChecked(), self.tot_pow.isChecked()))
        self.analyse_thread.start()
        
    def pausing(self):
        Analyse_C.on = False
        if not Analyse_C.in_loop:
            self.to_continue.setEnabled(True)
            self.to_pause.setEnabled(False)
            self.save_tab.setEnabled(True)

    def continueing(self):
        Analyse_C.on = True
        self.start_analyse()

    def stop_analyse(self):
        Analyse_C.on = False
        if not Analyse_C.in_loop:
            self.stop.setEnabled(False)
            self.apply.setEnabled(False)
            self.chfile.setEnabled(True)
            self.to_continue.setEnabled(False)
            self.to_pause.setEnabled(False)
            self.skip_row_box.setEnabled(True)
            self.rows_box.setEnabled(True)
            self.num_vals.setEnabled(True)
            self.num_times.setEnabled(True)
            self.save_tab.setEnabled(True)
            self.new_file.setEnabled(True)
            self.mob_pressure.setEnabled(True)
            self.tot_pow.setEnabled(True)

    def stop_app(self):
        Analyse_C.on = False
        Analyse_C.in_loop = False
        
    def update_min(self):
        self.rows_box.setMinimum(self.skip_row_box.value())

    def creat_new_file(self):
        file_name, _ = QFileDialog.getSaveFileName(caption="Make a new file", directory="", filter="CSV (*.csv);;Excel (*.xlsx)")
        try:
            if file_name.lower().endswith(".csv"):
                with open(file_name, 'w') as file:
                    file.write("t(s),I1 (A),I2 (A),I3 (A),V (V)")
            else:
                workbook = openpyxl.Workbook()
                sheet = workbook.active
                sheet["A1"] = 't(s)'
                sheet["B1"] = 'I1 (A)'
                sheet["C1"] = 'I2 (A)'
                sheet["D1"] = 'I3 (A)'
                sheet["E1"] = 'V (V)'
                workbook.save(file_name)
        except FileNotFoundError:
            return
        
    def save_opts(self):
        for file, opt_f in zip(self.files, Analyse_C.file_opts.values()):
            fl = file.split('/')[-1]
            file_name, _ = QFileDialog.getSaveFileName(caption=f"Save the results of {fl}", directory="", filter="Excel (*.xlsx)")
            try:
                workbook = openpyxl.Workbook()
                sheet = workbook.active
                index = 1

                for opt, charact in opt_f.items():
                    sheet["A"+str(index)] = f"{opt} :"
                    sheet["B"+str(index)] = "Number of use"
                    sheet["B"+str(index+1)] = charact['nb_of_use']
                    sheet["C"+str(index)] = "Stabal value"
                    sheet["C"+str(index+1)] = charact["stab_value"]
                    sheet["D"+str(index)] = "Start times"
                    sheet["E"+str(index)] = "End times"
                    sheet["F"+str(index)] = "Max value"
                    for i in range(len(charact['start_time'])):
                        index += 1
                        sheet["D"+str(index)] = charact['start_time'][i]
                        sheet["E"+str(index)] =  charact['end_time'][i]
                        sheet["F"+str(index)] = charact['max'][i]

                    index += 2
                workbook.save(file_name)
            except FileNotFoundError:
                return

app = QApplication(sys.argv)
UIWindow = App()
app.exec()