from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup
import bs4
from keras.utils import img_to_array
from keras.utils import load_img
from keras.models import load_model
from PIL import Image
from io import BytesIO
import requests
from urllib.parse import unquote
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import urllib.request
import numpy as np
import cv2
import time
import json
import os
from shinherpro import vfcModel
from shinherpro import chormeDriver
from shinherpro import logSave
import sys


###################################################
# V 1.7.1 By Yihuan --> 2023/7/7

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

global UserNameSave

def urlGet():
    return "https://sai.tyai.tyc.edu.tw/online/"

def setup(driverIn,modelIn):
    global driver,model
    driver = driverIn
    model = modelIn

def score_tolist(new_page_source):
    
    html = new_page_source
    soup = BeautifulSoup(html, 'html.parser')

    subject_scores = []
    rows = soup.select('table.t02 tr.row')
    for row in rows:
        subject = row.select_one('td.top').text.strip()
        score_elements = row.select('td.top.right span')
        if len(score_elements) >= 2:
            user_score = score_elements[0].text.strip()
            class_average = score_elements[1].text.strip()
            subject_scores.append({'考試科目': subject, '個人成績': user_score, '全班平均': class_average})
        else:
            subject_scores.append({'考試科目': subject, '個人成績': '未公布', '全班平均': '未公布'})

    total_score = soup.select_one('table.scoreTable-inline td.score').text.strip()

    average_score_elements = soup.select('table.scoreTable-inline td.score')
    average_score = average_score_elements[1].text.strip() if len(average_score_elements) >= 3 else "N/A"

    ranking_elements = soup.select('table.scoreTable-inline td.score')
    ranking = ranking_elements[2].text.strip() if len(ranking_elements) >= 3 else "N/A"
    department_ranking = ranking_elements[3].text.strip() if len(ranking_elements) >= 4 else "N/A"

    result = {
        'code': 0,
        '考試標題': soup.select_one('.center.pt-2 .bluetext').text.strip(),
        '學號': soup.select_one('.center.mobile-text-center .mr-3-ow:nth-of-type(1)').text.strip().replace('學號：', ''),
        '姓名': soup.select_one('.center.mobile-text-center .mr-3-ow:nth-of-type(2)').text.strip().replace('姓名：', ''),
        '班級': soup.select_one('.center.mobile-text-center .mr-3-ow:nth-of-type(3)').text.strip().replace('班級：', ''),
        '考試科目成績': subject_scores,
        '總分': total_score,
        '平均': average_score,
        '排名': ranking,
        '科別排名': department_ranking
    }

    return result

def logGenerate(start_time,result,vfcTry,vfcTryList):
    end_time = time.time()
    execution_time = end_time - start_time

    new_log = [
    {
        'runTime': execution_time,
        'VfcTry': vfcTry,
        'vfcTryList': vfcTryList
    }
    ]

    result['log'] = new_log
    return result

def login(username, password,LowConfidence=85,stepPrint=False):
    global UserNameSave
    UserNameSave = username
    driver.delete_all_cookies()
    driver.refresh()
    try:
        if stepPrint == False :
            sys.stdout = open(os.devnull, 'w')

        start_time = time.time()
        while True:
            allConfidence = 0
            vfcTry = 1
            vfcTryList = []

            while allConfidence <= LowConfidence :
                vfc = ""
                findImgCount = 0
                while(True):
                    findImgCount = findImgCount + 1
                    try:
                        imgvcode = driver.find_element(By.XPATH, '//img[@id="imgvcode"]')
                        break
                    except:
                        if findImgCount <= 3 :
                            driver.refresh()
                        else:
                            return {"code":1,'reason':[{'reason':'img[@id="imgvcode can\'t find'}]}

                src = imgvcode.get_attribute('src')
                print('Image source:', src)

                screenshot_path = 'captcha.png'
                driver.save_screenshot(screenshot_path)
                location = imgvcode.location
                size = imgvcode.size
                imgvcode_image = Image.open(screenshot_path)
                imgvcode_image = imgvcode_image.crop((location['x'], location['y'], location['x'] + size['width'], location['y'] + size['height']))
                width, height = imgvcode_image.size

                part_width = width // 4
                imgvcode_images = []
                for i in range(4):
                    left = i * part_width
                    right = (i + 1) * part_width
                    part = imgvcode_image.crop((left, 0, right, height))
                    part = vfcModel.vfcCodeFilter(part)
                    part_path = f'captcha_part{i}.png'
                    part.save(part_path)
                    imgvcode_images.append(part_path)

                confidence_threshold_low = 50
                confidence_threshold_medium = 80
                
                confidence = [0, 0, 0, 0]
                count = 0

                for imgvcode_image_path in imgvcode_images:
                    predicted_label, predicted_confidence = vfcModel.predict_image(imgvcode_image_path, imgvcode_image, model)
                    vfc += str(predicted_label)
                    predicted_confidence = predicted_confidence * 100
                    confidence[count] = predicted_confidence
                    count += 1

                    if predicted_confidence < confidence_threshold_low:
                        print(f"{RED}驗證碼: {predicted_label} 置信度: {predicted_confidence} %{RESET}")
                    elif predicted_confidence < confidence_threshold_medium:
                        print(f"{YELLOW}驗證碼: {predicted_label} 置信度: {predicted_confidence} %{RESET}")
                    else:
                        print(f"{GREEN}驗證碼: {predicted_label} 置信度: {predicted_confidence} %{RESET}")

                allConfidence = confidence[0] * confidence[1] * confidence[2] * confidence[3] * 0.000001
                print("\033[33m 驗證碼影像辨識:" + str(vfc) + "  本次準確率:" + str(allConfidence) + " % \033[0m")
                vfcTryList.append((vfc,allConfidence))
                if allConfidence <= LowConfidence :
                    driver.refresh()
            print("\033[36m 驗證碼準確率達標 \033[0m")

            vcode = vfc

            username_element = driver.find_element(By.ID, 'Loginid')
            username_element.send_keys(username)
            password_element = driver.find_element(By.ID, 'LoginPwd')
            password_element.send_keys(password)
            vcode_element = driver.find_element(By.ID, 'vcode')
            vcode_element.send_keys(vcode)
            login_button = driver.find_element(By.ID, 'btnLogin')
            login_button.click()

            try:
                alert = Alert(driver)
                popup_text = alert.text
                print(popup_text)
                alert.dismiss()
                if popup_text == "驗證碼輸入錯誤，請重新輸入。":
                    print("驗證碼輸入錯誤,重新嘗試")
                    vfcTryList.append("vfc wrong")
                    vfcTry = vfcTry + 1
                elif popup_text == "帳號或密碼錯誤,請重新登入!":
                    if stepPrint==False : sys.stdout = sys.__stdout__
                    returnLog = {'code':1,'runTime':time.time()-start_time,'result':False}
                    logSave.addLog("Login",UserNameSave,returnLog)
                    return returnLog
                else:
                    reason = popup_text
                    if stepPrint==False : sys.stdout = sys.__stdout__
                    returnLog = {'code':2,'runTime':time.time()-start_time,'result' : popup_text }
                    logSave.addLog("Login",UserNameSave,returnLog)
                    return returnLog
    
            except:
                print(f"{GREEN}密碼正確.{RESET}",end="")
                break

        print(f"{GREEN}驗證碼正確.{RESET}")
        if stepPrint==False : sys.stdout = sys.__stdout__
        returnLog = {'code':0,'runTime':time.time()-start_time,'result':True}
        logSave.addLog("Login",UserNameSave,returnLog)
        return returnLog
    except:
        returnLog = {'code':33,'runTime':time.time()-start_time,'reason':'something Wrong'}
        logSave.addLog("Login",UserNameSave,returnLog)
        return returnLog

def Credit_html_to_json(html):
    html_data = html

    soup = BeautifulSoup(html_data, 'html.parser')

    student_info = soup.find('div', class_='center').text.strip().split('\xa0')
    class_name = student_info[0].split('：')[1]
    seat_number = student_info[2].split('：')[1]
    student_id = student_info[4].split('：')[1]
    student_name = student_info[6].split('：')[1]

    subjects = []
    table_rows = soup.find('table', id='restudyList').find_all('tr')
    for row in table_rows[1:]:
        cells = row.find_all('td')
        subject_code = cells[0].text.strip() if cells[0].text else None
        subject_name = cells[1].text.strip() if cells[1].text else None
        retake_semester = cells[2].text.strip() if cells[2].text else None
        historical_records = cells[3].text.strip() if cells[3].text else None
        credits = cells[4].text.strip() if cells[4].text else None
        subjects.append({
            '科目代碼': subject_code,
            '科目名稱': subject_name,
            '重補修學期': retake_semester,
            '歷年成績記錄': historical_records,
            '學分': credits
        })

    electronic_rows = soup.find_all('tr', class_='電子二甲')
    electronic_contents = []
    for row in electronic_rows:
        cells = row.find_all('td')
        content = [cell.text.strip() if cell.text else None for cell in cells]
        electronic_contents.append(content)

    bt_rows = soup.find_all('tr', class_='bt')
    bt_contents = []
    for row in bt_rows:
        cells = row.find_all('td')
        content = [cell.text.strip() if cell.text else None for cell in cells]
        bt_contents.append(content)

    merged_contents = electronic_contents + bt_contents

    data = {
        '班級': class_name,
        '座號': seat_number,
        '學號': student_id,
        '姓名': student_name,
        '不及格科目': subjects,
        '學分': merged_contents,
    }

    json_data = json.dumps(data, ensure_ascii=False)
    return json_data,data


def getGrades(examname,stepPrint=False,justReturnHTML=False):
    driver.refresh()
    stepSave = 0
    try:
        stepSave = 1

        # 進入成績查詢頁面
        # 切換到左測選單
        chormeDriver.switch_frame(False, ["left"], driver)
        student_data_link = driver.find_element(By.ID, 'lnkStudentData')  # 按鈕名稱 "學生 xxx 的資料"
        student_data_link.click()
        # 尋找按鈕名稱 "查詢學生資料"
        button_name = '查詢學生資料'
        button_elements = driver.find_elements(By.CSS_SELECTOR, 'td.SubMenuItem') 
        for button in button_elements:
            button_text = button.text
            if button_text == button_name:
                button.click()
                break
                
        stepSave = 2

        # 切換到框架"right"的框架"right_below"
        chormeDriver.switch_frame(True, ["right", "right_below"], driver)
        # 找到查詢資料按鈕
        button = driver.find_element(By.CSS_SELECTOR, "button[onclick*='window.open']")
        button.click()
        # 切換到框架"right"的框架"right_below"
        chormeDriver.switch_frame(True, ["right", "right_top"], driver)
        # 找到各式成績查詢按鈕
        button = driver.find_element(By.XPATH, "//img[@title='各式成績查詢']")
        button.click()
        # 選擇彈出選擇考試的選單
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[-1])  # 切换到最新打开的窗口
        # 等待下拉框載入完成
        ddl_exam_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ddlExamList')))
        # 創建 Select 對象
        select = Select(ddl_exam_list)
        # 選擇下拉選單中的選項
        select.select_by_visible_text(examname)
        # 切换回原始窗口
        driver.switch_to.window(window_handles[0])
        
        stepSave = 3

        # 成績讀取

        # 切换到右侧框架
        chormeDriver.switch_frame(True, ["right", "right_below"], driver)
        # 獲取新窗口的頁面內容(成績表格)
        new_page_source = driver.page_source
        # 成績表格分析
        JsonGrade = score_tolist(new_page_source)
        loginScess = True

        driver.refresh()

        stepSave = 4

        JsonResult = JsonGrade

        if stepPrint==False : sys.stdout = sys.__stdout__
        
        logSave.addLog("GetGrade",UserNameSave,JsonResult)

        if justReturnHTML :
            return new_page_source
        else:
            return JsonResult


    except Exception as e:
        error_message = str(e) 
        if stepPrint == False:
            sys.stdout = sys.__stdout__

        JsonResult = {'code': 33, 'reason': f'something Wrong, step {stepSave}try的錯誤原應: {error_message}'}
        logSave.addLog("GetGrade",UserNameSave,JsonResult)
        return JsonResult

def getCredit(stepPrint=False):
    driver.refresh()
    try:
        stepSave = 1

        # 進入成績查詢頁面
        # 切換到左測選單
        chormeDriver.switch_frame(False, ["left"], driver)
        student_data_link = driver.find_element(By.ID, 'lnkStudentData')  # 按鈕名稱 "學生 xxx 的資料"
        student_data_link.click()

        button_element = driver.find_element(By.XPATH, '//a[text()="查詢各學期不及格科目"]')
        button_element.click()

        stepSave = 2
        driver.switch_to.default_content()
        chormeDriver.switch_frame(False,['right'],driver)

        new_page_source = driver.page_source

        driver.refresh()

        json_result = Credit_html_to_json(new_page_source)

        if stepPrint==False : sys.stdout = sys.__stdout__
        return json_result
    except:
        if stepPrint==False : sys.stdout = sys.__stdout__
        return {'code':33,'reason':f'something Wrong ,step {stepSave}'}
     
def getUserPhoto(username):
    driver.refresh()
    stepSave = 1
    try:
        chormeDriver.switch_frame(False, ["left"], driver)
    except:
        return {'code':1}
    student_data_link = driver.find_element(By.ID, 'lnkStudentData')  # 按鈕名稱 "學生 xxx 的資料"
    student_data_link.click()
    # 尋找按鈕名稱 "查詢學生資料"
    button_name = '查詢學生資料'
    button_elements = driver.find_elements(By.CSS_SELECTOR, 'td.SubMenuItem') 
    for button in button_elements:
        button_text = button.text
        if button_text == button_name:
            button.click()
            break
                
    stepSave = 2

    # 切換到框架"right"的框架"right_below"
    chormeDriver.switch_frame(True, ["right", "right_below"], driver)
    # 找到查詢資料按鈕
    button = driver.find_element(By.CSS_SELECTOR, "button[onclick*='window.open']")
    button.click()
    # 切換到框架"right"的框架"right_below"
    chormeDriver.switch_frame(True, ["right", "right_top"], driver)
    # 找到查詢基本資料按鈕
    button = driver.find_element(By.XPATH, "//img[@title='查詢基本資料']")
    button.click()
    chormeDriver.switch_frame(True, ["right","right_below"], driver)
    new_page_source = driver.page_source
    #print(new_page_source)
    soup = BeautifulSoup(new_page_source, 'html.parser')

    img_tag = soup.find('img')
    src = img_tag['src']

    url = "https://sai.tyai.tyc.edu.tw/online" + src[2:]
    img_element = driver.find_element(By.CSS_SELECTOR, 'img.lazyLoadImage')

    screenshot_path = 'PhotoSave\\screenshot.png'
    driver.save_screenshot(screenshot_path)

    location = img_element.location
    size = img_element.size

    x = location['x'] + 220
    y = location['y'] + 55
    width = size['width'] - 0
    height = size['height'] - 0

    screenshot = Image.open('PhotoSave\\screenshot.png')
    image_cropped = screenshot.crop((x, y, x + width, y + height))
    imgPath = 'PhotoSave\\UserPhoto' + username + '.png'
    image_cropped.save(imgPath)
    return {'code':0,'imgPath':imgPath,'url':url}

def getUserAbsentFromWork():
    driver.refresh()
    stepSave = 0
    try:
        stepSave = 1

        # 進入成績查詢頁面
        # 切換到左測選單
        chormeDriver.switch_frame(False, ["left"], driver)
        student_data_link = driver.find_element(By.ID, 'lnkStudentData')  # 按鈕名稱 "學生 xxx 的資料"
        student_data_link.click()
        # 尋找按鈕名稱 "查詢學生資料"
        button_name = '查詢學生資料'
        button_elements = driver.find_elements(By.CSS_SELECTOR, 'td.SubMenuItem') 
        for button in button_elements:
            button_text = button.text
            if button_text == button_name:
                button.click()
                break
                
        stepSave = 2

        # 切換到框架"right"的框架"right_below"
        chormeDriver.switch_frame(True, ["right", "right_below"], driver)
        # 找到查詢資料按鈕
        button = driver.find_element(By.CSS_SELECTOR, "button[onclick*='window.open']")
        button.click()
        # 切換到框架"right"的框架"right_below"
        chormeDriver.switch_frame(True, ["right", "right_top"], driver)
        # 找到各式成績查詢按鈕
        button = driver.find_element(By.XPATH, "//img[@title='查詢缺曠統計資料']")
        button.click()
        chormeDriver.switch_frame(True, ["right", "right_below"], driver)
        new_page_source = driver.page_source

        soup = BeautifulSoup(new_page_source, 'html.parser')
        rows = soup.find_all('tr')

        time_slots = ["早", "升", "1", "2", "3", "4", "午", "5", "6", "7", "8", "降", "9", "10", "11", "12"]
        special_dict = {"曠課": [], "公假": [], "請假": []}

        for row in rows[1:]:
            columns = row.find_all('td')
            
            # Get the date from the first column
            date = columns[0].get_text(strip=True)

            # Start from the second column and only handle existing columns
            for i, col in enumerate(columns[1: min(len(columns), len(time_slots) + 1)]):  # +1 for the date column
                text = col.get_text(strip=True)
                slot = time_slots[slot]
                if text == "缺":
                    special_dict["曠課"].append(f"{date} {slot}")
                elif text == "公":
                    special_dict["公假"].append(f"{date} {slot}")
                elif text == "事":
                    special_dict["請假"].append(f"{date} {slot}")

        json_output = json.dumps(special_dict, ensure_ascii=False, separators=(',', ':'))

        return json_output


    except Exception as e:
        error_message = str(e) 
        return {'code': 33, 'reason': f'something Wrong, step {stepSave}try的錯誤原應: {error_message}'}


def getAllData():

    # get user base data
    driver.refresh()
    stepSave = 1
    try:
        chormeDriver.switch_frame(False, ["left"], driver)
    except:
        return {'code':1}
    student_data_link = driver.find_element(By.ID, 'lnkStudentData')  # 按鈕名稱 "學生 xxx 的資料"
    student_data_link.click()
    # 尋找按鈕名稱 "查詢學生資料"
    button_name = '查詢學生資料'
    button_elements = driver.find_elements(By.CSS_SELECTOR, 'td.SubMenuItem') 
    for button in button_elements:
        button_text = button.text
        if button_text == button_name:
            button.click()
            break
                
    stepSave = 2

    # 切換到框架"right"的框架"right_below"
    chormeDriver.switch_frame(True, ["right", "right_below"], driver)
    # 找到查詢資料按鈕
    button = driver.find_element(By.CSS_SELECTOR, "button[onclick*='window.open']")
    button.click()
    # 切換到框架"right"的框架"right_below"
    chormeDriver.switch_frame(True, ["right", "right_top"], driver)
    # 找到查詢基本資料按鈕
    button = driver.find_element(By.XPATH, "//img[@title='查詢基本資料']")
    button.click()
    chormeDriver.switch_frame(True, ["right","right_below"], driver)
    new_page_source = driver.page_source
    #print(new_page_source)
    soup = BeautifulSoup(new_page_source, 'html.parser')

    list_items = soup.find_all('tr')
    bastDataList = []
    for count,item in enumerate(list_items):
        bastDataList.append([])
        for item2 in item.find_all('td'):
            bastDataList[count].append(item2.text)
    #print(bastDataList)
    studentID = bastDataList[0][2]
    studentName = bastDataList[0][4]
    studentGender = bastDataList[2][3]
    studentIdentity = bastDataList[2][1]
    studentEnglishName = bastDataList[6][1]
    studentClass = bastDataList[3][1]
    studentBirthday = bastDataList[1][1]
    studentJuniorHighSchool = bastDataList[11][1]
    studentInschool = bastDataList[13][1]

    UserBastData = {
        'schoolID':studentID,
        'name':studentName,
        'englishName':studentEnglishName,
        'gender':studentGender,
        'class':studentClass,
        'birthday':studentBirthday,
        'juniorHighSchool':studentJuniorHighSchool,
        'inschool':studentInschool,
        'identity':studentIdentity
    }

    #get life performance

    stepSave = 3

    
    # 切換到框架"right"的框架"right_below"
    chormeDriver.switch_frame(True, ["right", "right_top"], driver)
    # 找到查詢基本資料按鈕
    button = driver.find_element(By.XPATH, "//img[@title='查詢德育獎懲資料']")
    button.click()
    chormeDriver.switch_frame(True, ["right","right_below"], driver)
    new_page_source = driver.page_source
    #print(new_page_source)
    soup = BeautifulSoup(new_page_source, 'html.parser')

    list_items = soup.find_all('tr')
    lifeDataList = []
    for count,item in enumerate(list_items):
        lifeDataList.append([])
        for item2 in item.find_all('td'):
            lifeDataList[count].append(item2.text)

    award = {'嘉獎':lifeDataList[1][2],'小功':lifeDataList[1][4],'大功':lifeDataList[1][6]}
    punish = {'警告':lifeDataList[2][2],'小過':lifeDataList[2][4],'大過':lifeDataList[2][6]}
    record = []
    for item in lifeDataList[5:]:
        record.append(item)
    
    UserLifeData = {
        'award':award,
        'punish':punish,
        'record':record
    }

    YearExamList = ['一年級歷年成績','二年級歷年成績','三年級歷年成績','四年級歷年成績']
    YearDataList = []
    
    for YearExam in YearExamList:
        # 切換到框架"right"的框架"right_below"
        chormeDriver.switch_frame(True, ["right", "right_top"], driver)
        # 找到查詢基本資料按鈕
        button = driver.find_element(By.XPATH, "//img[@title='查詢歷年成績資料']")
        button.click()
        # 選擇彈出的選單
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[-1])  # 切换到最新打开的窗口
        # 等待下拉框載入完成
        ddl_exam_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'ddlItems1')))
        # 創建 Select 對象
        select = Select(ddl_exam_list)
        # 選擇下拉選單中的選項
        select.select_by_visible_text(YearExam)
        # 切换回原始窗口
        driver.switch_to.window(window_handles[0])
        # 成績讀取
        # 切换到右侧框架
        chormeDriver.switch_frame(True, ["right", "right_below"], driver)
        # 獲取新窗口的頁面內容(成績表格)
        new_page_source = driver.page_source
        #print(new_page_source)

        soup = BeautifulSoup(new_page_source, 'html.parser')
        list_items = soup.find_all('tr')
        oneYearDataList = []
        for count,item in enumerate(list_items):
            oneYearDataList.append([])
            for item2 in item.find_all('td'):
                oneYearDataList[count].append(item2.text)
        
        #print(oneYearDataList)

        sujectData = []
        for item in oneYearDataList[3:]:
            if len(item) != 8:
                break
            else:
                sujectData.append({
                    item[0]:{
                        '上學期':{
                            '屬性':item[1],
                            '學分':item[2],
                            '成績':item[3],
                        },
                        '下學期':{
                            '屬性':item[4],
                            '學分':item[5],
                            '成績':item[6],
                        },
                        '學年':item[7]
                    }
                })

        oneDataItem = {
            'year':oneYearDataList[0][0],
            'tag':oneYearDataList[2],
            'sujectData':sujectData
        }
        YearDataList.append({YearExam:oneDataItem})

    #get All exam data

    # 切換到框架"right"的框架"right_below"
    chormeDriver.switch_frame(True, ["right", "right_top"], driver)
    # 找到查詢基本資料按鈕
    button = driver.find_element(By.XPATH, "//img[@title='各式成績查詢']")
    button.click()
    # 選擇彈出選擇考試的選單
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])  # 切换到最新打开的窗口
    # 等待下拉框載入完成
    ddl_exam_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ddlExamList')))
    # 創建 Select 對象
    select = Select(ddl_exam_list)
    options = select.options
    allExamName = []
    for exam in options[2:]:
        allExamName.append(exam.text)

    Allexam = {}

    for exam in allExamName:

        # 選擇下拉選單中的選項
        select.select_by_visible_text(exam)
        # 切换回原始窗口
        driver.switch_to.window(window_handles[0])
        # 成績讀取
        # 切换到右侧框架
        chormeDriver.switch_frame(True, ["right", "right_below"], driver)
        # 獲取新窗口的頁面內容(成績表格)
        new_page_source = driver.page_source
        Allexam.update({exam:score_tolist(new_page_source)})

        # 切換到框架"right"的框架"right_below"
        chormeDriver.switch_frame(True, ["right", "right_top"], driver)
        # 找到查詢基本資料按鈕
        button = driver.find_element(By.XPATH, "//img[@title='各式成績查詢']")
        button.click()
        # 選擇彈出選擇考試的選單
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[-1])  # 切换到最新打开的窗口
        # 等待下拉框載入完成
        ddl_exam_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ddlExamList')))
        # 創建 Select 對象
        select = Select(ddl_exam_list)
        options = select.options

    # 選擇下拉選單中的選項
    select.select_by_visible_text(allExamName[0])
    # 切换回原始窗口
    driver.switch_to.window(window_handles[0])  
    

    UserCredit = getCredit()[1]

    #print(Allexam)

    return {'code':0,'UserBastData':UserBastData,'UserLifeData':UserLifeData,'YearDataList':YearDataList,'ALLExamData':Allexam,'UserCredit':UserCredit}