[install]

python 3.8x (tested on 3.8.10) (python3 이상, 너무 오래된 version만 아니면 됨.)

requests == 2.22.0

python-dotenv == 0.19.1

nltk == 3.6.5

https://github.com/helpdiana/help-diana-algorithm/tree/main/API_test 에서 ocr version 3 (v3)와 trans version 5 (v5) download

https://www.ncloud.com/ 에서 Papago text translation 에서 Application key 발급한 후,

Client ID (X-NCP-APIGW-API-KEY-ID), Client Secret(X-NCP-APIGW-KEY) 복사해서

앞서 다운 받은 translation python 코드에 아래와 같은 부분에 붙여넣기.

![image](https://user-images.githubusercontent.com/80442377/146261813-3c75848b-52ab-410f-8e0a-b8859863861f.png)

https://www.ncloud.com/ 에서 CLOVA OCR 도메인 생성한 후,

Secret Key, APIGW Invoke URL 값 복사해서

앞서 다운 받은 ocr python 코드에 아래와 같은 부분에 붙여넣기.

![image](https://user-images.githubusercontent.com/80442377/146261883-2aed38e8-0c6f-43e9-a0db-6c083deb1db1.png)

단어 사전 활용 git : https://github.com/helpdiana/help-diana-algorithm-be
