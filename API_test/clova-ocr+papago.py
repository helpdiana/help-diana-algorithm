##clova-ocr + papago api => 여러 사진 처리후 text파일 출력

import json
import base64
import requests
from dotenv import load_dotenv
import os
import sys
import urllib.request
import argparse
from nltk import sent_tokenize
import csv


    
def CLOVA_OCR(img) :
    URL = '' #naver cloud platform OCR api APIGW Invoke URL 
    KEY = '' #naver cloud platform OCR api Secret Key

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
    ocr_imsi  = []
    trans_imsi = []
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
        
        #한 문장씩 list형태로 저장
        ocr_imsi.append([sentence])
        trans_imsi.append([translatedText])
        
        #전송 형태 json
        ocr_dic = {
            "trans_before": ocr_imsi
        }
        trans_dic = {
            "trans_after": trans_imsi
        }

        #각 진단서의 마지막 문장이 입력되면 저장.
        #각각의 진단서 아웃풋 형태 : [ [문장1],[문장2],[문장3],...,[문장N]]
        if sentence is tokenized_sentences[-1] :
            #ocr 추출 결과 json으로 저장
            with open(f"{store_filepath}/ocr_{filename}.json", "w", encoding='utf-8') as of:
                json.dump(ocr_dic, of,ensure_ascii=False, indent="\t")
                
            #papago 번역 결과 json으로 저장
            with open(f"{store_filepath}/trans_{filename}.json", "w", encoding='utf-8') as pf:
                json.dump(trans_dic, pf,ensure_ascii=False, indent="\t")

    

    print("Done")
