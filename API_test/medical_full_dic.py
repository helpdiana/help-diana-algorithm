#약어 풀 네임 사전
# -*- encoding: utf-8 -*-
from os import error
import requests
import csv
from bs4 import BeautifulSoup

source_url = "https://terms.naver.com"
full_crawling_list = []

for page in range(1,357):
    req = requests.get("https://terms.naver.com/list.naver?cid=60408&categoryId=59580&so=st3.asc&viewType=&categoryType=&page={0}".format(page))
    soup = BeautifulSoup(req.text, 'html.parser')
    #index = soup.select('#content > div.contents_list_wrap.sub > ul.contents_list > li.contents_sub.active > ul > li > a')
    index = soup.select('#content > .list_wrap > ul > li')
    for i in range(0,len(index)):
        
        try:
            #print(i)
            detail_url = source_url+index[i].find("a")["href"]
            #print(detail_url)
            d_req = requests.get(detail_url)
            d_soup = BeautifulSoup(d_req.text, 'html.parser')



            key2 = d_soup.select('#content > div.section_wrap > div.headword_title > p.word > .word_txt')
            #print(key2[0].get_text())
            key2 = key2[0].get_text()

            #contents
            content = d_soup.select('#size_ct > p.txt')
            #print(content[0].get_text())
            content = content[0].get_text()
            #value
            value = content.split('.')[0]
            #print(value)

            full_crawling_list.append({'key':key2, 'value':value, 'content':content})

            full_keys = full_crawling_list[0].keys()
            #print()            
        except:
            pass
        
        
with open("./full_crawling_dictionary.csv", 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, full_keys)
    dict_writer.writeheader()
    dict_writer.writerows(full_crawling_list)
