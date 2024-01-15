from flask import Flask, request
from flask import render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit

import gspread

from google.oauth2 import service_account
from google.auth.transport.requests import Request

import tyaiShinher
import tyaiPracticeExam
import time
import json

app = Flask(__name__)
app.config['Json_AS_ASCII'] = False
app.config['SECRET_KEY'] = 'secret'
CORS(app)
socketio = SocketIO(app)

ngrok_code = "8926"


@app.route('/adduser')
def writeData():

    arg1 = request.args.get('schoolNumber')
    arg2 = request.args.get('studentID')
    arg3 = request.args.get('email')

    credentials = service_account.Credentials.from_service_account_file('shinherpro-411307-4f1771760028.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])

    spreadsheet_id = '1C3ZGa7ArEVRzH9hiox5Ggz-0jWrl9cHgD6Lc2STrWVQ'
    sheet_name = '工作表1'

    gc = gspread.Client(auth=credentials)
    spreadsheet = gc.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.worksheet(sheet_name)

    data_to_append = ["", arg1, arg2, arg3, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]

    b_column_data = worksheet.col_values(2)

    if data_to_append[1] not in b_column_data:
        worksheet.append_row(data_to_append)
        print("數據已成功添加到試算表。")
        response = "success"
    else:
        print("B列已經存在相同的宿。")
        response = "error"

    worksheet.append_row(data_to_append)

    print("數據已成功寫入試算表。")

    return response


@app.route('/adduser')
def adduser():
    
    try:
        start_time = time.time()

        arg1 = request.args.get('schoolNumber')
        arg2 = request.args.get('studentID')
        arg3 = request.args.get('email')

        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"Request processed in {elapsed_time} seconds")

    except:
        response = 'fail'

    return response

if __name__ == '__main__':

    socketio.run(app,host='0.0.0.0', port=80)