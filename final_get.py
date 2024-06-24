import tyaiShinher
import requests
import gspread
from google.oauth2 import service_account
from time import sleep
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import time
import random
from datetime import datetime

def calculate_absentees(absentee_data):
    total_absences = 0
    total_late = 0
    
    # 迭代每個缺席情況和年級學期
    for absentee_type, grade_data in absentee_data.items():

        if absentee_type == '遲到':
            for term_data in grade_data.values():
                total_late += term_data  # 累加遲到次數
        if absentee_type == '曠課':
            for term_data in grade_data.values():
                total_absences += term_data  # 累加遲到次數
    
    return total_absences, total_late


def send_mail(mailadd,data):

    file_path = 'gmail_password.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    gmail_user = 'shinherpro@gmail.com'
    gmail_password = file_content

    to_email = mailadd


    file_path = 'templates\\final.html'
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()


    if int(data['total_absences']) == 0:
        html_content = html_content.replace('3年來，優秀的你只曠課total_absences節','3年來，優秀的你從來沒有曠課！')

    html_content = html_content.replace('total_absences',str(data['total_absences']))
    html_content = html_content.replace('total_late',str(data['total_late']))
    html_content = html_content.replace('credit',str(data['credit']))
    html_content = html_content.replace('required',str(data['required']))
    html_content = html_content.replace('professional',str(data['professional']))
    html_content = html_content.replace('internship',str(data['internship']))


    print(int(data['username']))

    if int(data['username']) <13313:
        html_content = html_content.replace('你','妳')

    name = data['username']
    with open(f'save/{name}.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f'確定要送出給{name}嗎？')
    input()
    print(f'正在送出給{name}！')

    message = MIMEMultipart()
    message['From'] = gmail_user
    message['To'] = to_email
    message['Subject'] = "終點，一個新的開始!"

    html_part = MIMEText(html_content, 'html')
    message.attach(html_part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to_email, message.as_string())

    print('HTML Email sent successfully!')



credentials = service_account.Credentials.from_service_account_file('shinherpro-411307-4f1771760028.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])

spreadsheet_id = '1C3ZGa7ArEVRzH9hiox5Ggz-0jWrl9cHgD6Lc2STrWVQ'
sheet_name = '工作表1'

gc = gspread.Client(auth=credentials)
spreadsheet = gc.open_by_key(spreadsheet_id)
worksheet = spreadsheet.worksheet(sheet_name)

all_data = worksheet.get_all_values()

header = all_data[1]
users_data = all_data[2:]

users_list = []
for user_row in users_data:
    user_dict = dict(zip(header, user_row))
    users_list.append(user_dict)


print(f'user:{(users_list)}')


stop_couter = 0

for data in users_list:

    arg1 = data['user']
    arg2 = data['password']

    response = tyaiShinher.get_credit(arg1, arg2)
    print([response['Result']['合計實得學分'],response['Result']['必修通過百分比'],response['Result']['專業科目通過百分比'],response['Result']['實習科目通過百分比']])
    response2 = tyaiShinher.get_work(arg1, arg2)

    print(calculate_absentees(response2))


    mail_data = {
        'total_absences':calculate_absentees(response2)[0],
        'total_late': str(580-int(calculate_absentees(response2)[1])),
        'credit':str(int(response['Result']['合計實得學分'])),
        'required':response['Result']['必修通過百分比'],
        'professional':response['Result']['專業科目通過百分比'],
        'internship':response['Result']['實習科目通過百分比'],
        'username':data['user']
    }



    send_mail(data['email'],mail_data)


    stop_couter += 1

