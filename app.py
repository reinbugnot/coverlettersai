from flask import Flask, render_template, request, flash
from model.model_functions import get_completion, get_coverletter
from langchain.llms import OpenAI
from rq import Queue
from worker import conn
import openai
import os
import gunicorn

openai.api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(openai_api_key=openai.api_key)
q = Queue(connection=conn)

app = Flask(__name__)
#app.secret_key = "manbearpig_MUDMAN888"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        cv = request.form['cvtext']
        jd = request.form['jdtext']
        word_count = int(request.form['charcount'])

        app.logger.info('Generating Cover Letter...')
        job = q.enqueue(get_coverletter, cv, jd, word_count)

        cover_letter = get_coverletter(cv, jd, word_count)

        return render_template('index.html', output=cover_letter)
    else:
        return render_template('index.html', output='')

if __name__ == '__main__':
	app.run(debug=True)