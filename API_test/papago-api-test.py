import os
import sys
import urllib.request
client_id = "" # 개발자센터에서 발급받은 Client ID 값
client_secret = "" # 개발자센터에서 발급받은 Client Secret 값
t = ""#번역할 내용
encText = urllib.parse.quote(t)
#영어 -> 한국어 번역
data = "source=en&target=ko&text=" + encText
url = "https://openapi.naver.com/v1/papago/n2mt"
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request, data=data.encode("utf-8"))
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    # response_body -> byte string : decode to utf-8
    api_callResult =response_body.decode('utf-8')
    # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
    api_callResult = json.loads(api_callResult)
    # Final Result
    translatedText = api_callResult['message']['result']["translatedText"]
    print(translatedText)
else:
    print("Error Code:" + rescode)
    
    