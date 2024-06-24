from flask import Flask, request
from flask import render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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


def send_mail(mailadd,name,number):

    file_path = 'gmail_password.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    gmail_user = 'shinherpro@gmail.com'
    gmail_password = file_content

    to_email = mailadd

    subject = f'Hi!{name},歡迎使用shinherPro🙂'

    file_path = 'templates/cheakMail.html'
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    beta_user = ['013333','013314','013322','013325','013315','013304','013328','013335','013320','013308','013326','013321']

    # if number in beta_user:
    #     file_path = 'templates/betauser.html'
    #     with open(file_path, 'r', encoding='utf-8') as file:
    #         beta_html_content = file.read()
    #     html_content = html_content.replace('<!--beta User-->',beta_html_content)

    message = MIMEMultipart()
    message['From'] = gmail_user
    message['To'] = to_email
    message['Subject'] = subject

    html_part = MIMEText(html_content, 'html')
    message.attach(html_part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to_email, message.as_string())

    print('HTML Email sent successfully!')


@app.route('/examScore')
def example():
    start_time = time.time()

    arg1 = request.args.get('schoolNumber')
    arg2 = request.args.get('studentID')
    arg3 = request.args.get('examname')


    response = tyaiShinher.get_score(arg1, arg2,arg3)
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

def writeData(args,name,number):

    arg1 = args.get('schoolNumber')
    arg2 = args.get('studentID')
    arg3 = args.get('email')

    credentials = service_account.Credentials.from_service_account_file('shinherpro-411307-4f1771760028.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])

    spreadsheet_id = '1C3ZGa7ArEVRzH9hiox5Ggz-0jWrl9cHgD6Lc2STrWVQ'
    sheet_name = '工作表1'

    gc = gspread.Client(auth=credentials)
    spreadsheet = gc.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.worksheet(sheet_name)

    data_to_append = [arg1, arg2, arg3, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]

    b_column_data = worksheet.col_values(2)

    index_to_replace = None
    for i, value in enumerate(b_column_data):
        if str(data_to_append[0]) == value:
            
            index_to_replace = i+1

    if index_to_replace is not None:
        
        cell = worksheet.find(str(data_to_append[0]), in_column=2)
        worksheet.update(f'B{cell.row}:E{cell.row}', values=[data_to_append], value_input_option='RAW')
        print("數據已成功替換試算表中的相同行。")
        send_mail(arg3, name, number)
        response = "success"
    else:
        worksheet.append_row(data_to_append)
        print("數據已成功添加到試算表。")
        send_mail(arg3, name, number)
        response = "success"

    print("數據已成功寫入試算表。")

    return response



@app.route('/login')
def login():
    
    try:
        start_time = time.time()

        arg1 = request.args.get('schoolNumber')
        arg2 = request.args.get('studentID')
        arg3 = request.args.get('email')
        
        response = tyaiShinher.login(arg1, arg2)

        writeData(request.args,response,arg1)

        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"Request processed in {elapsed_time} seconds")

    except Exception as e:
        response = str(e)

    return response





if __name__ == '__main__':

    socketio.run(app,host='0.0.0.0', port=80)