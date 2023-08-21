from flask import Flask, render_template, request, flash, jsonify
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

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        cv = request.form['cvtext']
        jd = request.form['jdtext']
        word_count = int(request.form['charcount'])

        app.logger.info('Generating Cover Letter...')

        # Enqueue the job and get its ID
        job = q.enqueue(get_coverletter, cv, jd, word_count)
        job_id = job.get_id()

        # Return the job ID to the client
        return jsonify({ 'job_id': job_id }), 202
        #return render_template('index.html', output=cover_letter)
    else:
        return render_template('index.html', output='')
    
@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    job = q.fetch_job(job_key)

    if job.is_finished:
        return str(job.result), 200
    else:
        return "Nay!", 202


if __name__ == '__main__':
    app.run(debug=False)

    # Start gunicorn with a custom timeout duration
    # subprocess.call(['gunicorn', '--timeout', '90', 'app:app'])