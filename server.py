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

tester = '013333'
testerPassword = ''
examname = '期末考_1'

with open('testerPassword.txt', 'r', encoding='utf-8') as file:
    testerPassword= file.read()


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


print(f'user:{len(users_list)}')

base_url = f'http://xhinherpro.xamjiang.com/examScore?schoolNumber={tester}&studentID={testerPassword}&examname={examname}'
response = requests.get(base_url).text

#response = input('輸入json:')
response = json.loads(response)

last_result = []
for subject_data in response[0]['Subjects']:
        last_result.append(subject_data)

def send_mail(mailadd,examname,number,realscore,ranking,av):

    file_path = 'gmail_password.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    gmail_user = 'shinherpro@gmail.com'
    gmail_password = file_content

    to_email = mailadd

    subject = f'Hi!你的{examname}成績公布了!,快點進來看看🫢'

    file_path = 'templates\\score.html'
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()


    html_content = html_content.replace('##subject',examname)
    html_content = html_content.replace('##score',str(realscore))
    html_content = html_content.replace('##thisclassRank',str(ranking))
    html_content = html_content.replace('##thisIsAv',str(av))
    
    if realscore >= 60:
         html_content = html_content.replace('var(--MainGrade-color)','#00ff00')
    elif realscore >= 50:
         html_content = html_content.replace('var(--MainGrade-color)','#ffff00')
    else:
         html_content = html_content.replace('var(--MainGrade-color)','#ff0000')

    beta_user = ['013333','013314','013322','013325','013315','013304','013328','013335','013320','013308','013326','013321']

    if number in beta_user:
        file_path = 'templates\\betauser.html'
        with open(file_path, 'r', encoding='utf-8') as file:
            beta_html_content = file.read()
        html_content = html_content.replace('<!--beta User-->',beta_html_content)

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



while True:

    response = requests.get(base_url).text

    #response = input('輸入json:')
    response = json.loads(response)

    subjects_list = []
    print(response[0]['Subjects'])
    
    for subject_data in response[0]['Subjects']:
        subjects_list.append(subject_data)

    if len(subjects_list) > len(last_result):
        for i,sub in enumerate(subjects_list):
             if sub not in last_result:
                print(f'新增科目:{sub},序號{i}')
                 
                for user in users_list:
                    print(f'寄送給{user["email"]}')
                    
                    thisbase_url = f'http://xhinherpro.xamjiang.com/examScore?schoolNumber='+user['user']+ '&studentID=' + user['password'] +f'&examname={examname}'
                    print(thisbase_url)
                    thisresponse = requests.get(thisbase_url).text
                    #print(thisresponse)
                    thisresponse = json.loads(thisresponse)

                    this_result = []
                    for subject_data in thisresponse[0]['Subjects']:
                            this_result.append(subject_data)

                    send_mail(user['email'],this_result[i]['SubjectName'], user['user'], this_result[i]['Score'], this_result[i]['ClassRank'], round(this_result[i]['ClassAVGScore'], 2))
                    sleep(1)
    else:
        print('沒有新科目'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))                
    sleep(120+random.randint(0, 15)