import matplotlib.pyplot as plt

class plot:
    """Plots a real time data"""
    dis_colors = ['blue','yellow','red','orange','gray','green']
    operation_color = {}

    def __init__(self, x, **graphes):
        self.x = x
        self.graphes = graphes

    def plt_graph(self):
        
        plt.cla()
        for graph_name, graph in self.graphes.items():
            plt.plot(self.x[-len(graph):], graph, label=graph_name)
        plt.legend(loc='upper left')
        

    def shade(self, operations):
        for operation_name, operation in operations.items():
            if operation_name not in plot.operation_color.keys():
                plot.operation_color[operation_name] = plot.dis_colors[0]
                plot.dis_colors.pop(0)
            for start_time, end_time in zip(operation['start_time'],operation['end_time']):
                if start_time > self.x[0]:
                    plt.axvspan(start_time,end_time,color=plot.operation_color[operation_name], alpha=0.2)
                elif end_time > self.x[0]:
                    plt.axvspan(self.x[0],end_time,color=plot.operation_color[operation_name], alpha=0.2)
                    
        plt.pause(3)