from flask import Flask, render_template, request, flash
from model.model_functions import get_completion, get_coverletter
from langchain.llms import OpenAI

from rq import Queue
from worker import conn
import openai
import os

import gunicorn
import subprocess
import time

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

        # Wait for the task to complete before returning the result to the user
        while job.result is None:
            time.sleep(1)

        cover_letter = job.result

        return render_template('index.html', output=cover_letter)
    else:
        return render_template('index.html', output='')

if __name__ == '__main__':
    app.run(debug=False)

    # Start gunicorn with a custom timeout duration
    subprocess.call(['gunicorn', '--timeout', '90', 'app:app'])