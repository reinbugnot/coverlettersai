from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        cvtext = request.form['cvtext']
        jdtext = request.form['jdtext']
        charcount = request.form['charcount']
        
        # Some function
        output = cvtext + jdtext + charcount
        
        return render_template('index.html', output=output)
    else:
        return render_template('index.html', output='')


if __name__ == '__main__':
	app.run()