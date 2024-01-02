import requests

def get_score(student_number,student_password):

    login_url = 'https://score.exchuan.com.tw/iScore/identify/login_chk.php'
    data_url = 'https://score.exchuan.com.tw/iScore/Student/Exam/stuScore.php'

    login_payload = {
        'Type_No': '3',
        'Type_Name': 'Student',
        'tbLogin': student_number,
        'tbPasswd': student_password,
    }

    payload = {
        'sltExamID': 'ABC11202',
        'Sch_Stu': 'undefined',
    }

    session = requests.Session()

    response_login = session.post(login_url, data=login_payload)

    if response_login.status_code == 200:
        print('登入成功')
        
        response_data = session.post(data_url, data=payload)
        
        if response_data.status_code == 200:
            return response_data.text
        else:
            return '取得資料失敗，狀態碼:', response_data.status_code
    else:
        return '登入失敗，狀態碼:', response_login.status_code


