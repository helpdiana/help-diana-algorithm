# -*- encoding: utf-8 -*-
from os import error
import requests
import csv
from bs4 import BeautifulSoup

KOR_LIST = ["r", "s", "e", "f", "a", "q", "t", "d", "w", "c", "z", "x", "v", "g" ]
ENG_LIST = ["a", "b", "C", "d", "e", "f", "g", "h", "i" "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
BASE_URL = "http://www.kmle.co.kr/"

crawling_list = []
#BASE_URL_KOR = "http://www.kmle.co.kr/ebook_terminology_list.php?Kor="
#BASE_URL_ENG = "http://www.kmle.co.kr/ebook_terminology_list.php?Eng=&TitleLetter="

def crawl_dict_list_detail(urls):

    for url in urls:
        #print(url)
        try:
            detail_url = BASE_URL + url['href']
            detail_req = requests.get(detail_url)
            soup = BeautifulSoup(detail_req.text, 'html.parser')

            title = soup.select('h1')[0].text.strip()
            content = soup.select('.panel-body > p')[0].text.strip() 
            key, value = title.split(":")
            crawling_list.append({'key':key, 'value':value, 'content':content})
        except:
            pass    


def crawl_dict_list():
    
    for key in KOR_LIST:

        req = requests.get("http://www.kmle.co.kr/ebook_terminology_list.php?Kor={0}".format(key))
        soup = BeautifulSoup(req.text, 'html.parser')
            
        urls = soup.select(
            '.list-group-item'
        )
        crawl_dict_list_detail(urls)
        
     
    for key in ENG_LIST:
        req = requests.get("http://www.kmle.co.kr/ebook_terminology_list.php?Eng={0}&TitleLetter={1}".format(key, key.upper()))
        soup = BeautifulSoup(req.text, "html.parser")

        urls = soup.select(
            '.list-group-item'
        )
        crawl_dict_list_detail(urls)

        
    store_to_csv()
    
        
def store_to_csv():
    
    keys = crawling_list[0].keys()
    with open("crawling_dictionary_1.csv", 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(crawling_list)


def run():
    crawl_dict_list()



if __name__ == "__main__":
    run()