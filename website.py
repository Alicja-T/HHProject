from flask import Flask, render_template, request
from hakim_basic import Havel_Hakimi
from graph_visual import Graph_Visual

app=Flask(__name__)
@app.route("/")
def home():
  return render_template("home.html")

@app.route("/about/")
def about():
  return render_template("about.html")

@app.route("/success/", methods=['POST'])
def success():
    if request.method=='POST':
        sequence = request.form["userSequence"]
        seq = sequence.split(' ')
        i = 0
        for i in range(len(seq)):
            seq[i] = int(seq[i])
        sequence = seq[1:]
        hh = Havel_Hakimi(sequence)
        isGraphic = hh.is_graphic()
        script = ""
        div = ""
        cdn_js = ""
        cdn_css = ""
        print(isGraphic)
        if isGraphic:
            edges = hh.Max_HH()
            graph = Graph_Visual(sequence, edges)
            graph_data = graph.create_plot()
            script = graph_data[0]
            div = graph_data[1]
            cdn_js = graph_data[2]
            cdn_css = graph_data[3]

    return render_template("success.html", isGraphic = isGraphic, plot_script=script, plot_div=div, cdn_js=cdn_js, cdn_css=cdn_css)

if __name__=="__main__":
    app.run(debug=True)
