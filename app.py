from flask import Flask, render_template, request, flash
from model.model_functions import get_completion, get_coverletter
from langchain.llms import OpenAI
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(openai_api_key=openai.api_key)

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        cv = request.form['cvtext']
        jd = request.form['jdtext']
        word_count = int(request.form['charcount'])
        
        # Some function
        app.logger.info('Generating Cover Letter...')
        output = get_coverletter(cv, jd, word_count)
        
        return render_template('index.html', output=output)
    else:
        return render_template('index.html', output='Input Error, please try again')


if __name__ == '__main__':
	app.run(debug=True)