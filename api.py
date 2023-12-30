from flask import Flask, request
from get import get_score
import time

app = Flask(__name__)

@app.route('/getScore')
def example():
    start_time = time.time()

    arg1 = request.args.get('schoolNumber')
    arg2 = request.args.get('studentID')

    response = get_score(arg1, arg2)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Request processed in {elapsed_time} seconds")

    return f"Request processed in {elapsed_time} seconds\r\n" + response

if __name__ == '__main__':
    app.run(port=5000)
