# -*- coding: utf-8 -*-
#v5

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


client_id = "" #naver cloud platform에서 발급받은 client id 값
client_secret = "" #naver cloud platform에서 발급 받은 client scret 값


def papago(sentences,s1,s2):
    encText = urllib.parse.quote(sentences)
    data = "source={0}&target={1}&text=".format(s1,s2) + encText
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
    return translatedText



def Trans(path,filename):
    

    with open(f"{path}/{filename}", "r",encoding="UTF-8") as json_file:
        json_data = json.load(json_file)
        
        
    trans_img_imsi = []
    trans_total_imsi = []
    #img별로 접근
    for img in range(0,len(json_data['diagnose_eng_af'])):
        #img안의 문장별로 접근
        for sent in range(0,len(json_data['diagnose_eng_af'][img])):

            try:
                #papago 해석
                sentences = json_data['diagnose_eng_af'][img][sent][0]

                #papago api 유료ver
                #mid_translatedText = papago(sentences,s1 = 'ko', s2 = 'en')
                #print(mid_translatedText)
                #print()
                translatedText = papago(sentences,s1 = 'en', s2 = 'ko')
                #print(translatedText)
                #print()



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
                
                #해석 완료된거 리스트로 저장
                trans_img_imsi.append([translatedText])
            except:
                pass
            
        #img한장에 대해 번역 완료된 list를 total list에 append
        trans_total_imsi.append(trans_img_imsi)
        #다시 새로운 img번역을 처리하기 위해 초기화
        trans_img_imsi = []



    trans_dic = {
    "diagnose_af": trans_total_imsi
    }

    #papago 번역 결과
    with open(f"{path}/ko_trans_{filename}", "w", encoding='utf-8') as pf:
        #json.dump(trans_dic, pf,ensure_ascii=False, indent="\t")
        json.dump(trans_dic, pf,ensure_ascii=False)


parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, help = 'input total ocr json filepath')
parser.add_argument('filename', type=str, help = 'input total ocr json file name')

args = parser.parse_args()
trans_path = args.path
trans_filename = args.filename
Trans(trans_path,trans_filename)
print("Trans Done")

