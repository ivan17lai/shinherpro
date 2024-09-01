import requests
from bs4 import BeautifulSoup
import os



# <------------------------------------------------>

# Shinher Pro 1.1

# 1.0版本是為TYAI舊成績系統設計的 使用模擬遊覽器來操作 現在已經改用2.0版本
# 作為1.0版本的延伸 1.1改用 Requests 直接發送請求 
# 1.1目前是設計 For YKVS

# 筆記:
#  我研究了一下你上面的程式
#  大概改了兩個地方
#  1. 使用session來保持連線，讓取得首次連線和取得驗證碼圖片的要求在同一個連線中
#  2. 動態取得 RequestVerificationToken

# 之前結果會是 "操作逾時" 的原因應該就是沒有正確的RequestVerificationToken
# 因為我沒有帳號密碼，所以回傳結果都會是 "驗證碼錯誤" 或 "帳號密碼錯誤"
# 從這樣的回應來看，欣河系統應該把我當作正常的請求，才會去進行密碼比對，輸入正確的帳號密碼後，應該可以成功登入

account = "這裡填入你的帳號"
password = "這裡填入你的密碼"

# 接下來驗證碼會自動打開給你看
# 你需要手動輸入驗證碼

# <------------------------------------------------>



session = requests.Session()
# 這個session是最重要的，可以讓驗證碼圖片不會一直變動

# 第一步: 訪問首頁取得驗證碼圖片
url = 'https://eschool.ykvs.ntpc.edu.tw/online/'
response = session.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    img_tag = soup.find('img', {'id': 'imgvcode'})
    Request_Verification_Token = soup.find('input', {'name': '__RequestVerificationToken'})['value']

    print(f"Request_Verification_Token: {Request_Verification_Token}")
    
    if img_tag:
        img_url = img_tag['src']
        
        if not img_url.startswith('http'):
            img_url = url.rsplit('/', 1)[0] + '/' + img_url
        
        print(f"URL: {img_url}")
        
        img_response = session.get(img_url)
        
        if img_response.status_code == 200:
            with open('vcode_image.jpg', 'wb') as f:
                f.write(img_response.content)
            print("save:vcode_image.jpg")
            #這裡會打開驗證碼，你需要手動輸入驗證碼
            os.system('vcode_image.jpg')

        else:
            print(f"error:{img_response.status_code}")        


    else:
        print("找不到 imgvcode 元素")
else:
    print(f"error:{response.status_code}")


# 第二步: 發送登入請求
url = 'https://eschool.ykvs.ntpc.edu.tw/online/login.asp'

print("請輸入你看到的驗證碼:")
vcode = input()

data = {
    '__RequestVerificationToken': Request_Verification_Token,
    'division': 'senior',
    'Loginid': account,
    'LoginPwd': password,
    'Uid': '',
    'vcode': vcode
}

response = session.post(url, data=data)

if response.status_code == 200:
    print("最終結果:")
    print(response.text)
else:
    print(f"error:{response.status_code}")
