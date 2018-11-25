import math
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, Circle, StaticLayoutProvider
from bokeh.palettes  import Spectral10
from bokeh.embed import components
from bokeh.resources import CDN

class Graph_Visual:
    def __init__ (self, sequence, edges):
        self.sequence = sequence
        self.size = len(sequence)
        self.node_indices = list( range(self.size) )
        self.edges = edges

    def layout(self):
        if self.size < 10:
            circ = [i*2*math.pi/self.size for i in node_indices]
            y = [math.cos(i) for i in circ]
            x = [math.sin(i) for i in circ]
        return zip(x,y)
        if self.size > 10:
            circ = [i*2*math.pi/self.size for i in node_indices]
            y = [math.cos(i) for i in circ]
            x = [math.sin(i) for i in circ]
        return zip(x,y)

    def create_plot(self):
        plot = figure(title="Graph from sequence", x_range=(-1.1, 1.1),
        y_range=(-1.1,1.1), tools="", toolbar_location=None)

        colors = []
        for i in range(self.size):
            colors.append(Spectral10[i%10])
        graph = GraphRenderer()
        graph.node_renderer.data_source.data = dict(
            index=self.node_indices,
            fill_color=colors # it has to be done depending on size
        )
        graph.node_renderer.data_source.add(colors, 'color')
        graph.node_renderer.glyph = Circle(size=25, fill_color='color')


        start_points, end_points = map( list, zip(*self.edges) )

        graph.edge_renderer.data_source.data = dict(
            start = start_points,
            end = end_points
        )

        circ = [i*2*math.pi/self.size for i in self.node_indices]
        print(circ)
        y = [math.cos(i) for i in circ]
        x = [math.sin(i) for i in circ]
        print(x)
        print(y)

        graph_layout = dict(zip(self.node_indices, zip(x,y)))
        graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)
        plot.renderers.append(graph)
        plot.axis.visible = False
        plot.grid.visible = False
        plot.text(x, y, text=["%d" % i for i in self.sequence],
        text_baseline="middle", text_align="center")
        script, div = components(plot)
        cdn_js = CDN.js_files
        cdn_css = CDN.css_files
        return (script, div, cdn_js[0], cdn_css[0])

#vertices = [i for i in range(10)]
#edges = [[0, 1], [0, 2], [0, 3], [4, 5], [4, 6], [4, 7], [8, 9], [8, 1], [8, 2], [3, 5], [3, 6], [7, 9], [7, 1], [2, 5], [6, 9]]
#graph = Graph_Visual(vertices, edges)
#script, div = graph.create_plot()
#print(script)
#print(div)
