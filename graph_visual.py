import math
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, Circle, StaticLayoutProvider
from bokeh.palettes  import Spectral8

node_indices = [0, 1, 2, 3, 4]

plot = figure(title="My little Graph", x_range=(-1.1, 1.1),
y_range=(-1.1,1.1), tools="", toolbar_location=None)

graph = GraphRenderer()
graph.node_renderer.data_source.data = dict(
    index=node_indices,
    fill_color=Spectral8[:5]
)
graph.node_renderer.data_source.add(Spectral8[:5], 'color')
graph.node_renderer.glyph = Circle(size=25, fill_color='color')

start_points = [0, 1, 2, 3, 4, 1, 2]
end_points = [1, 2, 3, 4, 0, 3, 0]
graph.edge_renderer.data_source.data = dict(
    start = start_points,
    end = end_points
)

circ = [i*2*math.pi/8 for i in node_indices]
y = [math.cos(i) for i in circ]
x = [math.sin(i) for i in circ]

graph_layout = dict(zip(node_indices, zip(x,y)))
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)
plot.renderers.append(graph)
plot.axis.visible = False
plot.grid.visible = False
output_file("graph.html")
show(plot)
