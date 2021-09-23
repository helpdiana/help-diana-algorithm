##clova-ocr + papago api => 여러 사진 처리후 text파일 출력

import json
import base64
import requests
from dotenv import load_dotenv
import os
import sys
import urllib.request

    
def CLOVA_OCR(img) :
    URL = 'ocr API Gateway url' #ocr API Gateway url
    KEY = 'ocr secret key' #ocr secret key

    headers = {
        'Content-Type': 'application/json;UTF-8',
        "X-OCR-SECRET": KEY
    }



    data = {
        'version': 'V1',
        'requestId': 'test_ocr_edueman',
        'timestamp': 0, # 현재 시간
        'lang': 'ko',
        'images': [
            {
                'name': 'korea_history',
                'format': 'jpg',
                "data": img.decode('utf-8')
            }
        ]
    }


    data = json.dumps(data).encode('UTF-8')
    response = requests.post(URL, data=data, headers=headers)
    
    return response



for num in range(1,21):
    filename = "test{0}".format(num) 
    image_type = "png"


    with open(f"./{filename}.{image_type}", "rb") as f:
        img = base64.b64encode(f.read())


    response = CLOVA_OCR(img)
    res = json.loads(response.text)


    image = res['images']
    word_list = image[0]['fields']

    text = ""
    for word in word_list:
        text += ' ' + word['inferText']
        
        
    """
    #papago api
    
    client_id = "개발자센터에서 발급받은 Client ID 값"   # 개발자센터에서 발급받은 Client ID 값
    client_secret = "개발자센터에서 발급받은 Client Secret 값 "   # 개발자센터에서 발급받은 Client Secret 값    
    encText = urllib.parse.quote(text)
    data = "source=en&target=ko&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    response_body = response.read()
    trans_text = response_body.decode('utf-8') 
    """

    with open(f"./test_result.txt", "a", encoding='utf-8') as f:
        f.write(text)
        #f.write('\n \n')
        #f.write(trans_text)
        f.write('\n \n \n \n \n \n')



    print("Done")