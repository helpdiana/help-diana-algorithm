# -*- encoding: utf-8 -*-
from os import error
import requests
import csv
from bs4 import BeautifulSoup


base_url = "https://terms.naver.com/list.naver?cid=66149&categoryId=66149"
source_url = "https://terms.naver.com"
crawling_list = []
req = requests.get(base_url)
soup = BeautifulSoup(req.text, 'html.parser')
#index = soup.select('#content > div.contents_list_wrap.sub > ul.contents_list > li.contents_sub.active > ul > li > a')
index = soup.select('.contents_sub.active > ul > li')


for i in range(0,len(index)):
    #print(i)
    detail_url = source_url+index[i].find("a")["href"]
    #print(detail_url)
    d_req = requests.get(detail_url)
    d_soup = BeautifulSoup(d_req.text, 'html.parser')
    value = d_soup.select('#content > div.section_wrap > div.headword_title > h2')
    #print(value[0].get_text()) # --> value
    value = value[0].get_text()
    key = d_soup.select('#content > div.section_wrap > div.headword_title > p.word > .word_txt')
    #print(key[0].get_text())
    key = key[0].get_text()
    content = d_soup.select('#size_ct > p.txt')
    #print(content[0].get_text())
    content = content[0].get_text()
    crawling_list.append({'key':key, 'value':value, 'content':content})
    
    keys = crawling_list[0].keys()
    with open("./crawling_dictionary_test.csv", 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(crawling_list)
    

print(crawling_list[0])
print(crawling_list[1])
print(crawling_list[2044])
print(len(crawling_list))