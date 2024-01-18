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

tester = '013333'
testerPassword = ''
examname = '期末考_1'
#examname = '期中考2_1'

with open('testerPassword.txt', 'r', encoding='utf-8') as file:
    testerPassword= file.read()

score_box_html = '''

<div class="subjectbox" style="max-width:30px">
    <div class="rectangle" style="height:##thisishigh2;background-color:#ffffff"></div>
    <div style="text-align:center;color:var(--text-color);font-size:12">##thisisscore</div>
    <div class="rectangle" style="background-color:##thisiscolor;height:##thisishigh;max-width:30px"></div>
    <div style="text-align:center;color:var(--text-color);font-size:12">##thisissub</div>
</div>

'''

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

def send_mail(mailadd,examname,number,realscore,ranking,av,all_data):

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

    current_time = datetime.now().time()
    hour = current_time.hour
    head_text = ''
    if 6 <= hour < 11:
        head_text = 'Hi!早安😇'
    elif 12 <= hour < 18:
        head_text = 'Hi!午安🫡'
    else:
        head_text = 'Hi!晚安😴'

    html_content = html_content.replace('##headText',head_text)

    if realscore >= 60:
         html_content = html_content.replace('var(--MainGrade-color)','#00ff00')
    elif realscore >= 50:
         html_content = html_content.replace('var(--MainGrade-color)','#ffe400')
    else:
         html_content = html_content.replace('var(--MainGrade-color)','#ff0000')

    if av >= 60:
         html_content = html_content.replace('var(--classAverage-color)','#00ff00')
    elif av >= 50:
         html_content = html_content.replace('var(--classAverage-color)','#ffe400')
    else:
         html_content = html_content.replace('var(--classAverage-color)','#ff0000')


    def get_color(score):
        if score >= 60:
            return '#00ff00'
        elif score >= 50:
            return '#ffe400'
        else:
            return '#ff0000'

    html_content = html_content.replace('var(--UserAverage-color)',get_color(ranking)) 


    all_score_box_html = ''
    for subject_data in all_data:

        this_score = score_box_html
        this_score = this_score.replace('##thisiscolor',get_color(subject_data['Score']))
        this_score = this_score.replace('##thisissub',subject_data['SubjectName'])
        this_score = this_score.replace('##thisishigh2', str(150-(subject_data['Score']*1.5))+'px')
        this_score = this_score.replace('##thisishigh', str(subject_data['Score']*1.5)+'px')

        this_score = this_score.replace('##thisisscore', str(int(subject_data['Score'])))
        all_score_box_html += this_score

    html_content = html_content.replace('<!-- ##thisIsTable -->',all_score_box_html)


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
                
                mail_save = []

                for user in users_list:

                    print(f'查詢{user["email"]}')
                    
                    thisbase_url = f'http://xhinherpro.xamjiang.com/examScore?schoolNumber='+user['user']+ '&studentID=' + user['password'] +f'&examname={examname}'
                    print(thisbase_url)
                    thisresponse = requests.get(thisbase_url).text
                    #print(thisresponse)
                    #thisresponse = input('輸入json22:')
                    thisresponse = json.loads(thisresponse)

                    this_result = []
                    for subject_data in thisresponse[0]['Subjects']:
                            this_result.append(subject_data)

                    allAv = 0
                    sub_s = {
                        '國語文' : 2,
                        '新聞英語' : 2,
                        '英語文' : 2,
                        '物聯網' : 3,
                        '基本網路分析' : 3,
                        '體育' : 2,
                        '應用數學' : 2,
                        '電子電路' : 3,
                        '生活科技' : 1,
                    }
                    scount = 0
                    ssum = 0
                    for sub in this_result:
                        try:
                            ssum += sub['Score'] * sub_s[sub['SubjectName']]
                            scount += sub_s[sub['SubjectName']]
                        except:
                            print('sub not found')
                            pass
                    
                    allAv = ssum / scount


                    mail_save.append(
                        { 'email' : user['email'],
                          'sub' : this_result[i]['SubjectName'],
                          'user' : user['user'],
                          'score' : this_result[i]['Score'],
                          'classRank' : this_result[i]['ClassRank'],
                          'ClassAVGScore' : round(this_result[i]['ClassAVGScore'], 2),
                          'this_result' : this_result,
                          'allAv' : round(allAv, 2),
                        }
                    )

                



                for mails in mail_save:

                    print(f'寄送給{mails["email"]}')
                    send_mail(mails['email'],mails['sub'],mails['user'],mails['score'],mails['allAv'],mails['ClassAVGScore'],mails['this_result'])
                    sleep(1)


        last_result = subjects_list
    else:
        print('沒有新科目'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))                
    sleep(120+random.randint(0, 15))