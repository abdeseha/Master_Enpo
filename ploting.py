import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class plot:
    """Plots a real time data"""
    def __init__(self, x, **graphes):
        self.x = x
        self.graphes = graphes

    def set_anime(self):
        
        plt.cla()
        for graph_name, graph in self.graphes.items():
            plt.plot(self.x, graph, label=graph_name)
    
        plt.legend(loc='upper left')
        plt.pause(3)