import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class plot:
    """Plots a real time data"""
    def __init__(self, x, **graphes):
        self.x = x
        self.graphes = graphes

    def set_anime(self):
        
        plt.cla()
        for graph in self.graphes:
            plt.plot(self.x, graph, label = str(graph))
    
        plt.legend(loc='upper left')
        plt.tight_layout()

    def animate (self):
        ani = FuncAnimation(plt.gcf(), plot.animate, interval=1000)
        plt.show()