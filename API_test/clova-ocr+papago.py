##clova-ocr + papago api
##command line 명령어 : python clova-ocr+papago.py [사진 폴더 주소] [결과 저장 주소] 입력


import json
import base64
import requests
from dotenv import load_dotenv
import os
import sys
import urllib.request
import argparse
from nltk import sent_tokenize


    
def CLOVA_OCR(img) :
    URL = ''
    KEY = ''

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


parser = argparse.ArgumentParser()
parser.add_argument('ocr_file_path', type=str, help = 'input ocr image filepath')
parser.add_argument('store_file_path', type=str, help = 'input store image filepath')

args = parser.parse_args()
ocr_filepath = args.ocr_file_path
store_filepath = args.store_file_path

img_list = os.listdir(ocr_filepath)
img_list.remove('.DS_Store')
#print(img_list)
img_list = sorted(img_list)

for img in img_list :

    filename = img
    with open(f"{ocr_filepath}/{filename}", "rb") as f:
        img = base64.b64encode(f.read())

    response = CLOVA_OCR(img)
    res = json.loads(response.text)

    image = res['images']
    word_list = image[0]['fields']

    text = ""
    for word in word_list:
        text += ' ' + word['inferText']
        
        
    tokenized_sentences = sent_tokenize(text)
    
    
    for sentence in tokenized_sentences:
        
        #papago api 유료ver
        client_id = "" #naver cloud platform에서 발급받은 client id 값
        client_secret = "" #naver cloud platform에서 발급 받은 client scret 값
        encText = urllib.parse.quote(sentence)
        data = "source=en&target=ko&text=" + encText
        url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
        request.add_header("X-NCP-APIGW-API-KEY",client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        response_body = response.read()
        # response_body -> byte string : decode to utf-8
        api_callResult =response_body.decode('utf-8')
        # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
        api_callResult = json.loads(api_callResult)
        # Final Result
        translatedText = api_callResult['message']['result']["translatedText"]
        
        """
        #papago api 무료ver

        client_id = "" # 개발자센터에서 발급받은 Client ID 값
        client_secret = "" # 개발자센터에서 발급받은 Client Secret 값    
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


        #ocr 추출 결과
        with open(f"{store_filepath}/ocr_{filename}.txt", "a", encoding='utf-8') as f:
            f.write(sentence)
            f.write('\n \n')
            
        #papago 번역 결과
        with open(f"{store_filepath}/trans_{filename}.txt", "a", encoding='utf-8') as f:
            f.write(translatedText)
            f.write('\n \n')
            
    print("Done")

    
    
    