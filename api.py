from flask import Flask, request
from flask import render_template
import tyaiShinher
import tyaiPracticeExam
import time
import json
app = Flask(__name__)


@app.route('/examScore')
def example():
    start_time = time.time()

    arg1 = request.args.get('schoolNumber')
    arg2 = request.args.get('studentID')

    response = tyaiShinher.get_score(arg1, arg2)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Request processed in {elapsed_time} seconds")

    return response

@app.route('/practiceExamScore')
def example2():
    start_time = time.time()

    arg1 = request.args.get('schoolNumber')
    arg2 = request.args.get('studentID')

    response = tyaiPracticeExam.get_score(arg1, arg2)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Request processed in {elapsed_time} seconds")

    return response


@app.route('/work')
def get_work():
    start_time = time.time()

    arg1 = request.args.get('schoolNumber')
    arg2 = request.args.get('studentID')

    response = tyaiShinher.get_work(arg1, arg2)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Request processed in {elapsed_time} seconds")

    return json.dumps(response, ensure_ascii=False, indent=2)

@app.route('/web')
def get_web():

    return render_template('main.html')

@app.route('/login')
def login():
    
    try:
        start_time = time.time()

        arg1 = request.args.get('schoolNumber')
        arg2 = request.args.get('studentID')

        response = tyaiShinher.login(arg1, arg2)
        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"Request processed in {elapsed_time} seconds")

    except:
        response = 'fail'

    return response


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)