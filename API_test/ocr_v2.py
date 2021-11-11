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


def OCR(path):
    img_list = os.listdir(path)
    #img_list.remove('.DS_Store')
    #print(img_list)
    img_list = sorted(img_list)
    
    for name in sorted(img_list):
        #print(name)
        suffix=os.path.splitext(name)[-1].lower()
        #print(suffix)
        #print("----")
        if suffix not in ['.gif', '.jpg', '.jpeg', '.png', '.bmp']:
            #print("n")
            #print(suffix)
            #print(name)
            img_list.remove(name)
            #print(file_list)
            #print("--------------==============================================--------------")


    for img in sorted(img_list) :

        filename = img
        with open(f"{path}/{filename}", "rb") as f:
            img = base64.b64encode(f.read())

        
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
        
        res = json.loads(response.text)

        image = res['images']
        word_list = image[0]['fields']

        text = ""
        for word in word_list:
            text += ' ' + word['inferText']


        tokenized_sentences = sent_tokenize(text)
        ocr_imsi  = []
        for sentence in tokenized_sentences:

            ocr_imsi.append([sentence])

            

            if sentence is tokenized_sentences[-1] :
                ocr_dic = {
                "trans_before": ocr_imsi
                }
                #ocr 추출 결과`
                with open(f"{path}/ocr_{filename}.json", "w", encoding='utf-8') as of:
                    #json.dump(ocr_dic, of,ensure_ascii=False, indent="\t")
                    json.dump(ocr_dic, of,ensure_ascii=False)


    print("OCR Done")


    
    
parser = argparse.ArgumentParser()
parser.add_argument('ocr_file_path', type=str, help = 'input ocr image filepath')
#parser.add_argument('store_file_path', type=str, help = 'input store image filepath')

args = parser.parse_args()
ocr_filepath = args.ocr_file_path
#store_filepath = args.store_file_path
OCR(ocr_filepath)
