import math
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, Circle, StaticLayoutProvider
from bokeh.palettes  import Spectral10
from bokeh.embed import components, autoload_static
from bokeh.resources import CDN

class Graph_Visual:
    def __init__ (self, sequence, edges):
        self.sequence = sequence
        self.size = len(sequence)
        self.node_indices = list( range(self.size) )
        self.edges = edges

    def layout(self):
        x = []
        y = []
        if self.size < 10:
            circ = [i*2*math.pi/self.size for i in self.node_indices]
            y = [math.cos(i) for i in circ]
            x = [math.sin(i) for i in circ]
            return zip(x,y)
        if 50 >= self.size >= 10:
            circ = [i*2*math.pi/self.size for i in self.node_indices]
            half = self.size/2
            for i in self.node_indices:
                if i % 2 == 0:
                    y.append( math.cos(circ[i]) )
                    x.append( math.sin(circ[i]) )
                else:
                    y.append( math.cos(circ[i])/2 )
                    x.append( math.sin(circ[i])/2 )
            return zip(x,y)
        if self.size > 50:
            grid_size = math.ceil( math.sqrt(self.size) )
            span = 2/grid_size

            for i in range(grid_size):
                for j in range(grid_size):
                    x.append(-1 + i*span)
                    y.append(-1 + j*span)
            return zip(x,y)

    def create_plot(self):
        plot = figure( x_range=(-1.1, 1.1),
        y_range=(-1.1,1.1), tools="", toolbar_location=None)

        colors = []
        for i in range(self.size):
            colors.append(Spectral10[i%10])
        graph = GraphRenderer()
        graph.node_renderer.data_source.data = dict(
            index=self.node_indices,
            fill_color=colors
        )
        graph.node_renderer.data_source.add(colors, 'color')
        graph.node_renderer.glyph = Circle(size=25, fill_color='color')
        plot.sizing_mode = 'scale_width'

        start_points, end_points = map( list, zip(*self.edges) )
        print(start_points)
        print(end_points)
        graph.edge_renderer.data_source.data = dict(
            start = start_points,
            end = end_points
        )
        coordinates = self.layout()
        coordinates_list = list(coordinates)
        print(coordinates_list)
        graph_layout = dict( zip(self.node_indices, coordinates_list) )
        graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

        plot.renderers.append(graph)
        plot.axis.visible = False
        plot.grid.visible = False
        x = []
        y = []
        for item in coordinates_list:
            x.append(item[0])
            y.append(item[1])
        plot.text(x, y, text=["%d" % i for i in self.sequence],
        text_baseline="middle", text_align="center")
        script, div = components(plot)
        cdn_js = CDN.js_files[0]
        cdn_css = CDN.css_files[0]
        js, tag = autoload_static(plot, CDN, "c:/temp")
        print(js)
        print(tag)
        return (script, div, cdn_js, cdn_css)

#vertices = [i for i in range(10)]
#edges = [[0, 1], [0, 2], [0, 3], [4, 5], [4, 6], [4, 7], [8, 9], [8, 1], [8, 2], [3, 5], [3, 6], [7, 9], [7, 1], [2, 5], [6, 9]]
#graph = Graph_Visual(vertices, edges)
#script, div, cdn1, cdn2 = graph.create_plot()
#coords = list( graph.layout() )
#data = graph.create_plot()
#print(script)
#print(div)
