import requests
import gspread
from google.oauth2 import service_account
from time import sleep

tester = '013333'
testerPassword = ''
examname = '期中考2_1'

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

while True:

    base_url = f'http://xhinherpro.xamjiang.com/examScore?schoolNumber={tester}&studentID={testerPassword}&examname={examname}'
    response = requests.get(base_url)

    subjects_list = []

    for subject_data in response.json()[0]['Subjects']:
        subjects_list.append(subject_data)

    for subject in subjects_list:
        print(subject['SubjectName'])

    sleep(3)