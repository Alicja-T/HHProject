import os
from flask import Flask, render_template, request, redirect, url_for
from hakim_basic import Havel_Hakimi
from graph_visual import Graph_Visual
from werkzeug import secure_filename

UPLOAD_FOLDER = '/home/emunah/mysite/uploads'
UPLOAD_FOLDER2 = 'c:/temp'
ALLOWED_EXTENSIONS = set(['txt'])
DIV_PREFIX = """<div class="form-row">
                    <div class="form-group col-md-10">
             """
BUTTON_PREFIX = """<div class="form-group col-md-2"><button class="btn btn-info ml-auto" name="confirm" type="submit" value="graph"""
BUTTON_SUFIX = """.html"> See graph </button></div>
                </div>
            """

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

@app.route("/results", methods=['GET', 'POST'])
def results():
    if request.method=='POST':
        filename = request.form['confirm']
        print("got you result "+filename)
    return render_template(filename)

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
        error = ""
        filename = request.form['confirm']
        filepath = UPLOAD_FOLDER2 + '/' + filename
        numbers = []
        file = open(filepath, "r")
        for val in file.read().split():
            numbers.append( int(val) )
        i = 0
        sequences = []
        invalid_file = False
        while i < len(numbers):
            count = numbers[i]
            sequence = []
            while count > 0:
                i += 1
                if (i < len(numbers)):
                    sequence.append(numbers[i])
                else:
                    invalid_file = True
                    break
                count -= 1
            sequences.append(sequence)
            i += 1
        print(invalid_file)
        if (not invalid_file):
            div = ""
            script = ""
            i = 0
            for seq in sequences:
                hh = Havel_Hakimi(seq)
                isGraphic = hh.is_graphic()
                print(isGraphic)
                if isGraphic:
                    i += 1
                    div += DIV_PREFIX + "Sequence: " + str(seq) + " is Graphic! </div>"
                    edges = hh.Max_HH()
                    graph = Graph_Visual(seq, edges)
                    graph_data = graph.create_plot(i)
                    div += BUTTON_PREFIX + str(i) + BUTTON_SUFIX
                else:
                    div += DIV_PREFIX + "Sequence: " + str(seq) + " is not Graphic!</div>"
        else:
            div = "your file is invalid"
        print(div)
    return render_template("file_analysis.html", error=invalid_file, result_div = div)


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
            edges = hh.Ur_HH()
            graph = Graph_Visual(sequence, edges)
            graph_data = graph.create_plot()
            script = graph_data[0]
            div = graph_data[1]
            cdn_js = graph_data[2]
            cdn_css = graph_data[3]

    return render_template("success.html", isGraphic = isGraphic, plot_script=script, plot_div=div, cdn_js=cdn_js, cdn_css=cdn_css)

if __name__=="__main__":
    app.run(debug=True)
