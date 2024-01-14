import requests
from bs4 import BeautifulSoup
import json

def convert_json_to_data(json_data):
    data = []

    student_info = json_data["Result"]
    student_name = student_info["StudentName"]
    student_class = student_info["StudentClassName"]
    student_seat_no = student_info["StudentSeatNo"]

    exam_info = student_info["ExamItem"]
    total_score = exam_info["TotalScore"]
    class_rank = exam_info["ClassRank"]
    department_rank = exam_info["DepartmentRank"]

    subject_info_list = student_info["SubjectExamInfoList"]
    subjects = []
    for subject_info in subject_info_list:
        subject = {
            "SubjectName": subject_info["SubjectName"],
            "Score": subject_info["Score"],
            "Flunk": subject_info["Flunk"],
            "ClassAVGScore": subject_info["ClassAVGScore"],
            "ClassRank": subject_info["ClassRank"],
        }
        subjects.append(subject)

    data.append({
        "StudentName": student_name,
        "StudentClass": student_class,
        "StudentSeatNo": student_seat_no,
        "TotalScore": total_score,
        "ClassRank": class_rank,
        "DepartmentRank": department_rank,
        "Subjects": subjects,
    })
    result_json_str = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8').decode('utf-8')
    
    return result_json_str

def login(student_number,student_id):

    login_url = 'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/Auth/CloudLogin'
    check_url = 'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/Auth/DoCloudLoginCheck'
    getCloudSuc_url = r'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/Auth/CloudLoginSuccess'
    page1_url = 'https://shcloud11.k12ea.gov.tw/TYAITYC/ICampus/StudentInfo/Index?page=%E5%AD%B8%E7%94%9F%E5%9F%BA%E6%9C%AC%E8%B3%87%E6%96%99'
    getScore_url = 'https://shcloud11.k12ea.gov.tw/TYAITYC/ICampus/CommonData/GetStudentBasicInfo'

    session = requests.Session()

    response_get = session.get(login_url)
    soup = BeautifulSoup(response_get.text, 'html.parser')
    token_element = soup.find('input', {'name': '__RequestVerificationToken'})

    if token_element:
        token_value = token_element['value']
        #print(f"__RequestVerificationToken: {token_value}")
    else:
        print("找不到__RequestVerificationToken欄位")


    cookies = session.cookies
    # print('--------------------------------------------------------------')
    # for cookie in cookies:
    #     print(cookie.name, cookie.value)
    # print('--------------------------------------------------------------')

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '286',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'shcloud11.k12ea.gov.tw',
        'Origin': 'https://shcloud11.k12ea.gov.tw',
        'Referer': 'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/Auth/CloudLogin',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    data = {
        'SchoolCode': '030403',
        'LoginId': student_number,
        'PassString': student_id,
        'LoginType': 'Student',
        'IsKeepLogin': 'false',
        'SchoolName': '%E5%8C%97%E7%A7%91%E9%99%84%E5%B7%A5',
        'GoogleToken': '',
        '__RequestVerificationToken': 'UJt9if8pkn7VG6eAUStF4iwL08-mt_8_x6Aj2DQ5dz7H7Vrd2nV4XbcckM5nVlot2VVoFSH_0OyV-0tz90lFqQnsJJJxIvG4rAmeZps5iXo1'
    }


    response_post = session.post(check_url, data=data, headers=headers,cookies=session.cookies)
    # print(response_post.text)

    # cookies = session.cookies
    # print('---------cloudlogin------------------------------------------')
    # for cookie in cookies:
    #     print(cookie.name, cookie.value)
    # print('--------------------------------------------------------------')

    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'shcloud11.k12ea.gov.tw',
        'Referer': 'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/Auth/CloudLogin',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows'
    }

    response_getCloudSuc = session.get(getCloudSuc_url, headers=headers,cookies=session.cookies)

    # print(response_getCloudSuc.text)
    # cookies = session.cookies
    # print('---------getCloudSuc------------------------------------------')
    # for cookie in cookies:
    #     print('CO::'+cookie.name, cookie.value)
    # print('--------------------------------------------------------------')


    url2_url = 'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/Authentication/GetEMailIsNotVaild'


    # print('try')


    cookies = session.cookies

    # for cookie in cookies:
    #     print(cookie.name, cookie.value)
    
    # print('-----------------------------------------------------------------------------')

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'shcloud11.k12ea.gov.tw',
        'Referer': 'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/Auth/CloudLoginSuccess',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    response = session.get(page1_url, headers=headers, cookies=session.cookies)

    soup = BeautifulSoup(response.text, 'html.parser')

    token_element = soup.find('input', {'name': '__RequestVerificationToken'})

    if token_element:
        token_value = token_element['value']
        # print(f"__RequestVerificationToken: {token_value}")
    else:
        print("找不到__RequestVerificationToken欄位")


    second_post_data = {
        'Year': '112',
        'Term': '1',
        'studentNo': student_number,
        '__RequestVerificationToken' : token_value
    }

    response_second_post = session.post(getScore_url, data=second_post_data, headers=headers,cookies=session.cookies)

    print(response_second_post.json()['Result']['StudentName'])

    return response_second_post.json()['Result']['StudentName']



def get_score(student_number,student_id):

    login_url = 'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/Auth/CloudLogin'
    check_url = 'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/Auth/DoCloudLoginCheck'
    getCloudSuc_url = r'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/Auth/CloudLoginSuccess'
    auth_url = 'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/'
    page1_url = 'https://shcloud11.k12ea.gov.tw/TYAITYC/ICampus/StudentInfo/Index?page=%E5%AD%B8%E7%94%9F%E5%9F%BA%E6%9C%AC%E8%B3%87%E6%96%99'
    getScore_url = 'https://shcloud11.k12ea.gov.tw/TYAITYC/ICampus/TutorShGrade/GetScoreForStudentExamContent'

    session = requests.Session()

    response_get = session.get(login_url)
    soup = BeautifulSoup(response_get.text, 'html.parser')
    token_element = soup.find('input', {'name': '__RequestVerificationToken'})

    if token_element:
        token_value = token_element['value']
        #print(f"__RequestVerificationToken: {token_value}")
    else:
        print("找不到__RequestVerificationToken欄位")


    cookies = session.cookies
    # print('--------------------------------------------------------------')
    # for cookie in cookies:
    #     print(cookie.name, cookie.value)
    # print('--------------------------------------------------------------')

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '286',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'shcloud11.k12ea.gov.tw',
        'Origin': 'https://shcloud11.k12ea.gov.tw',
        'Referer': 'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/Auth/CloudLogin',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    data = {
        'SchoolCode': '030403',
        'LoginId': student_number,
        'PassString': student_id,
        'LoginType': 'Student',
        'IsKeepLogin': 'false',
        'SchoolName': '%E5%8C%97%E7%A7%91%E9%99%84%E5%B7%A5',
        'GoogleToken': '',
        '__RequestVerificationToken': 'UJt9if8pkn7VG6eAUStF4iwL08-mt_8_x6Aj2DQ5dz7H7Vrd2nV4XbcckM5nVlot2VVoFSH_0OyV-0tz90lFqQnsJJJxIvG4rAmeZps5iXo1'
    }


    response_post = session.post(check_url, data=data, headers=headers,cookies=session.cookies)
    # print(response_post.text)

    # cookies = session.cookies
    # print('---------cloudlogin------------------------------------------')
    # for cookie in cookies:
    #     print(cookie.name, cookie.value)
    # print('--------------------------------------------------------------')

    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'shcloud11.k12ea.gov.tw',
        'Referer': 'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/Auth/CloudLogin',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows'
    }

    response_getCloudSuc = session.get(getCloudSuc_url, headers=headers,cookies=session.cookies)

    # print(response_getCloudSuc.text)
    # cookies = session.cookies
    # print('---------getCloudSuc------------------------------------------')
    # for cookie in cookies:
    #     print('CO::'+cookie.name, cookie.value)
    # print('--------------------------------------------------------------')


    url2_url = 'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/Authentication/GetEMailIsNotVaild'


    # print('try')


    cookies = session.cookies

    # for cookie in cookies:
    #     print(cookie.name, cookie.value)
    
    # print('-----------------------------------------------------------------------------')

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'shcloud11.k12ea.gov.tw',
        'Referer': 'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/Auth/CloudLoginSuccess',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    response = session.get(page1_url, headers=headers, cookies=session.cookies)

    soup = BeautifulSoup(response.text, 'html.parser')

    token_element = soup.find('input', {'name': '__RequestVerificationToken'})

    if token_element:
        token_value = token_element['value']
        # print(f"__RequestVerificationToken: {token_value}")
    else:
        print("找不到__RequestVerificationToken欄位")


    second_post_data = {
        'StudentNo': student_number,
        'SearchType': '單次考試所有成績',
        '__RequestVerificationToken': token_value,
        'Year': '112',
        'Term': '1',
        'ExamNo': '期中考2_1'
    }

    response_second_post = session.post(getScore_url, data=second_post_data, headers=headers,cookies=session.cookies)

    # print(response_second_post.text)

    return convert_json_to_data(response_second_post.json())

def organize_absent_data(json_data):
    result = json_data["Result"]
    organized_data = {}

    for entry in result:
        absent_type = entry["AbsentType"]
        organized_data[absent_type] = {
            "FirstGradeFirstTerm": entry["FirstGradeFirstTerm"],
            "FirstGradeSecondTerm": entry["FirstGradeSecondTerm"],
            "SecondGradeFirstTerm": entry["SecondGradeFirstTerm"],
            "SecondGradeSecondTerm": entry["SecondGradeSecondTerm"],
            "ThirdGradeFirstTerm": entry["ThirdGradeFirstTerm"],
            "ThirdGradeSecondTerm": entry["ThirdGradeSecondTerm"],
            "FourthGradeFirstTerm": entry["FourthGradeFirstTerm"],
            "FourthGradeSecondTerm": entry["FourthGradeSecondTerm"],
            "FifthGradeFirstTerm": entry["FifthGradeFirstTerm"],
            "FifthGradeSecondTerm": entry["FifthGradeSecondTerm"],
        }

    return organized_data

def get_work(student_number,student_id):

    login_url = 'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/Auth/CloudLogin'
    check_url = 'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/Auth/DoCloudLoginCheck'
    getCloudSuc_url = r'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/Auth/CloudLoginSuccess'
    auth_url = 'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/'
    page1_url = 'https://shcloud11.k12ea.gov.tw/TYAITYC/ICampus/StudentInfo/Index?page=%E5%AD%B8%E7%94%9F%E5%9F%BA%E6%9C%AC%E8%B3%87%E6%96%99'
    getScore_url = 'https://shcloud11.k12ea.gov.tw/TYAITYC/ICampus/TutorShSheAbsentStatistics/GetTutorShSheAbsentStatistics'

    session = requests.Session()

    response_get = session.get(login_url)
    soup = BeautifulSoup(response_get.text, 'html.parser')
    token_element = soup.find('input', {'name': '__RequestVerificationToken'})

    if token_element:
        token_value = token_element['value']
        # print(f"__RequestVerificationToken: {token_value}")
    else:
        print("找不到__RequestVerificationToken欄位")


    cookies = session.cookies
    # print('--------------------------------------------------------------')
    # for cookie in cookies:
    #     print(cookie.name, cookie.value)
    # print('--------------------------------------------------------------')

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '286',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'shcloud11.k12ea.gov.tw',
        'Origin': 'https://shcloud11.k12ea.gov.tw',
        'Referer': 'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/Auth/CloudLogin',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    data = {
        'SchoolCode': '030403',
        'LoginId': student_number,
        'PassString': student_id,
        'LoginType': 'Student',
        'IsKeepLogin': 'false',
        'SchoolName': '%E5%8C%97%E7%A7%91%E9%99%84%E5%B7%A5',
        'GoogleToken': '',
        '__RequestVerificationToken': 'UJt9if8pkn7VG6eAUStF4iwL08-mt_8_x6Aj2DQ5dz7H7Vrd2nV4XbcckM5nVlot2VVoFSH_0OyV-0tz90lFqQnsJJJxIvG4rAmeZps5iXo1'
    }


    response_post = session.post(check_url, data=data, headers=headers,cookies=session.cookies)
    # print(response_post.text)

    # cookies = session.cookies
    # print('---------cloudlogin------------------------------------------')
    # for cookie in cookies:
    #     print(cookie.name, cookie.value)
    # print('--------------------------------------------------------------')

    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'shcloud11.k12ea.gov.tw',
        'Referer': 'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/Auth/CloudLogin',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows'
    }

    response_getCloudSuc = session.get(getCloudSuc_url, headers=headers,cookies=session.cookies)

    # print(response_getCloudSuc.text)
    # cookies = session.cookies
    # print('---------getCloudSuc------------------------------------------')
    # for cookie in cookies:
    #     print('CO::'+cookie.name, cookie.value)
    # print('--------------------------------------------------------------')


    url2_url = 'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/Authentication/GetEMailIsNotVaild'


    # print('try')


    cookies = session.cookies

    # for cookie in cookies:
    #     print(cookie.name, cookie.value)
    
    # print('-----------------------------------------------------------------------------')

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'shcloud11.k12ea.gov.tw',
        'Referer': 'https://shcloud11.k12ea.gov.tw/TYAITYC/Auth/Auth/CloudLoginSuccess',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    response = session.get(page1_url, headers=headers, cookies=session.cookies)

    soup = BeautifulSoup(response.text, 'html.parser')

    token_element = soup.find('input', {'name': '__RequestVerificationToken'})

    if token_element:
        token_value = token_element['value']
        # print(f"__RequestVerificationToken: {token_value}")
    else:
        print("找不到__RequestVerificationToken欄位")

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'shcloud11.k12ea.gov.tw',
        'Origin': 'https://shcloud11.k12ea.gov.tw',
        'Referer': 'https://shcloud11.k12ea.gov.tw/TYAITYC/ICampus/StudentInfo/Index?page=%E5%AD%B8%E7%94%9F%E5%9F%BA%E6%9C%AC%E8%B3%87%E6%96%99',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    data = {
        'studentNo': student_number,
        '__RequestVerificationToken': token_value,
    }

    response_second_post = session.post(getScore_url, data=data, headers=headers,cookies=session.cookies)

    # print(response_second_post.text)

    return organize_absent_data(response_second_post.json())
