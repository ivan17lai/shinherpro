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




def send_mail(mailadd):

    file_path = 'gmail_password.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    gmail_user = 'shinherpro@gmail.com'
    gmail_password = file_content

    to_email = mailadd


    file_path = 'templates\\final.html'
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()



    message = MIMEMultipart()
    message['From'] = gmail_user
    message['To'] = to_email
    message['Subject'] = "終點，一個新的開始！"

    html_part = MIMEText(html_content, 'html')
    message.attach(html_part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to_email, message.as_string())

    print('HTML Email sent successfully!')


send_mail("ivan17.lai@gmail.com")
send_mail("std1013335@goo.tyai.tyc.edu.tw")