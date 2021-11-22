#약어사전
# -*- encoding: utf-8 -*-
from os import error
import requests
import csv
from bs4 import BeautifulSoup

source_url = "https://terms.naver.com"
short_crawling_list = []

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

            # --> key 약어
            key = d_soup.select('#content > div.section_wrap > div.headword_title > h2') 
            #print(key[0].get_text()) 
            key = key[0].get_text()

            #contents
            content = d_soup.select('#size_ct > p.txt')
            #print(content[0].get_text())
            content = content[0].get_text()
            #value
            value = content.split('.')[0]
            #print(value)

            short_crawling_list.append({'key':key, 'value':value, 'content':content})


            short_keys = short_crawling_list[0].keys()
            #print()
        except:
            pass

with open("./abbreviation_crawling_dictionary.csv", 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, short_keys)
    dict_writer.writeheader()
    dict_writer.writerows(short_crawling_list)
                
