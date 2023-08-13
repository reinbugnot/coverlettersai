from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"

@app.route("/", methods=['GET', 'POST'])
def home():
	return render_template("index.html")

@app.route('/output', methods=['POST'])
def output():
    cvtext = request.form.get('cvtext')
    jdtext = request.form.get('jdtext')
    targetcharcount = request.form.get('targetcharcount')
    return render_template("output.html")

if __name__ == '__main__':
	app.run()