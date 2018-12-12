import math
import io
from jinja2 import Template
from bokeh.plotting import figure, output_file, save
from bokeh.models import GraphRenderer, Circle, StaticLayoutProvider
from bokeh.palettes  import Spectral10
from bokeh.embed import components, autoload_static
from bokeh.resources import CDN
from hakim_basic import Havel_Hakimi

TEMPLATE_PATH1 = 'C:\\Users\\Aliza\\Dropbox\\Python\\HHproject\\templates\\graph'
SAVE_PATH = '/home/emunah/mysite/uploads/graph'

class Graph_Visual:
    def __init__ (self, sequence, edges):
        self.sequence = sequence
        self.size = len(sequence)
        self.node_indices = list( range(self.size) )
        self.edges = edges
        self.cdn_js = CDN.js_files[0]
        self.cdn_css = CDN.css_files[0]
        self.html_prefix = """{%extends "layout.html"%}
                                {%block content%}
                            """
        self.html_sufix = """{%endblock%}"""
        self.template = Template("""\
            <link rel="stylesheet" href={{cdn_css | safe }} type="text/css" />
            <script type="text/javascript" src={{cdn_js | safe}}></script>
            <div class="result">
            <button onclick="goBack()">Go Back</button>
                <script>
                    function goBack() {
                    window.history.back();
                    }
                </script>
                {{plot_script | safe}}
                {{plot_div | safe}}
            </div>
            """)

    def layout(self):
        x = []
        y = []
        if self.size < 10:
            circ = [i*2*math.pi/self.size for i in self.node_indices]
            y = [math.cos(i) for i in circ]
            x = [math.sin(i) for i in circ]
            return zip(x,y)
        if 50 >= self.size >= 10:
            half = self.size/2
            for i in self.node_indices:
                if i >= half:
                    circ = i*2*math.pi/half
                    y.append( math.cos(circ) )
                    x.append( math.sin(circ) )
                else:
                    circ = i*2*math.pi/half
                    y.append( math.cos(circ)/2 )
                    x.append( math.sin(circ)/2 )
            return zip(x,y)
        if self.size > 50:
            grid_size = math.ceil( math.sqrt(self.size) )
            span = 2/grid_size

            for i in range(grid_size):
                for j in range(grid_size):
                    x.append(-1 + i*span)
                    y.append(-1 + j*span)
            return zip(x,y)

    def create_plot(self, save_number=0):
        title1 = str(self.sequence) + " Max Havel-Hakimi"
        title2 = str(self.sequence) + " ParR HH x = 1"
        title3 = str(self.sequence) + " ParR HH x = 0"
        title4 = str(self.sequence) + " ParR HH x = -1"
        title5 = str(self.sequence) + " Min Havel-Hakimi"

        plot1 = figure(title=title1, title_location="below", x_range=(-1.1, 1.1),
        y_range=(-1.1,1.1), tools="", toolbar_location=None)

        plot2 = figure(title=title2, title_location="below", x_range=(-1.1, 1.1),
        y_range=(-1.1,1.1), tools="", toolbar_location=None)

        plot3 = figure(title=title3, title_location="below", x_range=(-1.1, 1.1),
        y_range=(-1.1,1.1), tools="", toolbar_location=None)

        plot4 = figure(title=title4, title_location="below", x_range=(-1.1, 1.1),
        y_range=(-1.1,1.1), tools="", toolbar_location=None)

        plot5 = figure(title=title5, title_location="below", x_range=(-1.1, 1.1),
        y_range=(-1.1,1.1), tools="", toolbar_location=None)

        colors = []
        for i in range(self.size):
            colors.append(Spectral10[i%10])

        graph1 = GraphRenderer()
        graph2 = GraphRenderer()
        graph3 = GraphRenderer()
        graph4 = GraphRenderer()
        graph5 = GraphRenderer()

        glyphs_colors = dict(
            index = self.node_indices,
            fill_color=colors
        )

        graph1.node_renderer.data_source.data = glyphs_colors
        graph2.node_renderer.data_source.data = glyphs_colors
        graph3.node_renderer.data_source.data = glyphs_colors
        graph4.node_renderer.data_source.data = glyphs_colors
        graph5.node_renderer.data_source.data = glyphs_colors

        hh = Havel_Hakimi(self.sequence)
        edges1 = hh.Max_HH()
        edges2 = hh.Parr_HH(1)
        edges3 = hh.Parr_HH(0)
        print(edges3)
        edges4 = hh.Parr_HH(-1)
        print(edges4)
        edges5 = hh.Min_HH()
        print(edges5)

        graph1.node_renderer.data_source.add(colors, 'color')
        graph1.node_renderer.glyph = Circle(size=25, fill_color='color')
        graph2.node_renderer.data_source.add(colors, 'color')
        graph2.node_renderer.glyph = Circle(size=25, fill_color='color')
        graph3.node_renderer.data_source.add(colors, 'color')
        graph3.node_renderer.glyph = Circle(size=25, fill_color='color')
        graph4.node_renderer.data_source.add(colors, 'color')
        graph4.node_renderer.glyph = Circle(size=25, fill_color='color')
        graph5.node_renderer.data_source.add(colors, 'color')
        graph5.node_renderer.glyph = Circle(size=25, fill_color='color')
        plot1.sizing_mode = 'scale_width'
        plot2.sizing_mode = 'scale_width'
        plot3.sizing_mode = 'scale_width'
        plot4.sizing_mode = 'scale_width'
        plot5.sizing_mode = 'scale_width'

        if (len(edges1) > 0):
            start_points, end_points = map( list, zip(*edges1) )
            graph1.edge_renderer.data_source.data = dict(
                start = start_points,
                end = end_points
            )
            start_points, end_points = map( list, zip(*edges2) )
            graph2.edge_renderer.data_source.data = dict(
                start = start_points,
                end = end_points
            )
            start_points, end_points = map( list, zip(*edges3) )
            graph3.edge_renderer.data_source.data = dict(
                start = start_points,
                end = end_points
            )
            start_points, end_points = map( list, zip(*edges4) )
            graph4.edge_renderer.data_source.data = dict(
                start = start_points,
                end = end_points
            )
            start_points, end_points = map( list, zip(*edges5) )
            graph5.edge_renderer.data_source.data = dict(
                start = start_points,
                end = end_points
            )

        coordinates = self.layout()
        coordinates_list = list(coordinates)
        graph_layout = dict( zip(self.node_indices, coordinates_list) )
        graph1.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)
        graph2.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)
        graph3.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)
        graph4.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)
        graph5.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

        plot1.renderers.append(graph1)
        plot1.axis.visible = False
        plot1.grid.visible = False

        plot2.renderers.append(graph2)
        plot2.axis.visible = False
        plot2.grid.visible = False

        plot3.renderers.append(graph3)
        plot3.axis.visible = False
        plot3.grid.visible = False

        plot4.renderers.append(graph4)
        plot4.axis.visible = False
        plot4.grid.visible = False

        plot5.renderers.append(graph5)
        plot5.axis.visible = False
        plot5.grid.visible = False
        x = []
        y = []
        for item in coordinates_list:
            x.append(item[0])
            y.append(item[1])

        plot1.text(x, y, text=["%d" % i for i in self.sequence],
        text_baseline="middle", text_align="center")
        plot2.text(x, y, text=["%d" % i for i in self.sequence],
        text_baseline="middle", text_align="center")
        plot3.text(x, y, text=["%d" % i for i in self.sequence],
        text_baseline="middle", text_align="center")
        plot4.text(x, y, text=["%d" % i for i in self.sequence],
        text_baseline="middle", text_align="center")
        plot5.text(x, y, text=["%d" % i for i in self.sequence],
        text_baseline="middle", text_align="center")
        plots = {'Max_HH' : plot1, 'Min_HH' : plot2, 'Ur_HH': plot3}

        script, div = components((plot1, plot2, plot3, plot4, plot5))
        div_better = ""
        for item in div:
            div_better+=item.strip()
        if save_number > 0:
            filename = TEMPLATE_PATH1 + str(save_number) + '.html'
            html = self.template.render( cdn_js = self.cdn_js,
                                        cdn_css = self.cdn_css,
                                        plot_script = script,
                                        plot_div = div
            )
            html = self.html_prefix + html + self.html_sufix
            with open(filename, 'w') as file:
                file.write(html)

        return (script, div_better, self.cdn_js, self.cdn_css)


#vertices = [i for i in range(10)]
#edges = [[0, 1], [0, 2], [0, 3], [4, 5], [4, 6], [4, 7], [8, 9], [8, 1], [8, 2], [3, 5], [3, 6], [7, 9], [7, 1], [2, 5], [6, 9]]
#graph = Graph_Visual(vertices, edges)
#script, div, cdn1, cdn2 = graph.create_plot()
#coords = list( graph.layout() )
#data = graph.create_plot()
#print(script)
#print(div)
