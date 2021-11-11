# -*- coding: utf-8 -*-

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


def Trans(path):
    
    file_list = os.listdir(path)
    #print(file_list)
    file_list = sorted(file_list)
    if '.DS_Store' in file_list:
        file_list.remove('.DS_Store')
        
    for x in sorted(file_list):
        if x[-4:] != 'json' :
            file_list.remove(x)
            
    #print(file_list)
    
    
    for img in file_list :

        filename = img
        #print(filename)
        #print(type(filename))
        #print(f"{path}/{filename}")

        with open(f"{path}/{filename}", "r",encoding="UTF-8") as json_file:
            json_data = json.load(json_file)
            
        json_list = json_data["trans_before"]
        trans_imsi = []
        for n in range(0,len(json_list)):
            sentence = json_list[n][0]
        
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

            trans_imsi.append([translatedText])
            
            if sentence is json_list[-1][0] :
                trans_dic = {
                "trans_after": trans_imsi
                }
                
                #papago 번역 결과
                with open(f"{path}/trans_{filename}", "w", encoding='utf-8') as pf:
                    #json.dump(trans_dic, pf,ensure_ascii=False, indent="\t")
                    json.dump(trans_dic, pf,ensure_ascii=False)




    print("Trans Done")


parser = argparse.ArgumentParser()
parser.add_argument('ocr_file_path', type=str, help = 'input ocr image filepath')
#parser.add_argument('store_file_path', type=str, help = 'input store image filepath')

args = parser.parse_args()
ocr_filepath = args.ocr_file_path
#store_filepath = args.store_file_path
Trans(ocr_filepath)