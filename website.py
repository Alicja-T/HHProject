import os
from flask import Flask, render_template, request, redirect, url_for
from hakim_basic import Havel_Hakimi
from graph_visual import Graph_Visual
from werkzeug import secure_filename

UPLOAD_FOLDER = '/home/emunah/mysite/uploads'
UPLOAD_FOLDER2 = 'c:/temp'
ALLOWED_EXTENSIONS = set(['txt'])

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER2

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/about/")
def about():
  return render_template("about.html")

@app.route("/upload/", methods=['GET', 'POST'])
def upload():
    if request.method=='POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template("upload.html", filename=filename)

@app.route("/file_analysis", methods=['POST'])
def file_analysis():
    if request.method=='POST':
        print(request.form)
    return render_template("upload.html")


@app.route("/success/", methods=['GET', 'POST'])
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
