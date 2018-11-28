# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import base64
from urllib.parse import urlparse
import os

#url="http://jandan.net/ooxx/page-36#comments"
url="http://jandan.net/ooxx"
def _base64_decode(data):
	return base64.b64decode(data)

def saveimage(url):
	image=requests.get(url)
	path=urlparse(url).path
	filenames=re.split('/',path)

	if os.path.exists("D:/src/xxoo") == False:
		os.mkdir("D:/src/xxoo")

	f = open("D:/src/xxoo/"+filenames[2], 'wb')
	f.write(image.content)
	f.flush()
	f.close()



def get_urls(url):
	headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Host': 'jandan.net'
    }
	
	html = requests.get(url, headers=headers).text
	#print(html)
	soup=BeautifulSoup(html,'html.parser')
	xxoos=soup.find_all('span',{'class':'img-hash'})
	#page=soup.find_all('span',{'class':'current-comment-page'})
	#curpage=page[1].text
	#curnum=curpage[1:3]
	#print("curpage is -------"+curnum)
	for xxoo in xxoos:
		#print(xxoo.string)
		print("img url:http:"+str(_base64_decode(xxoo.string),'utf-8'))
		imgurl="http:"+str(_base64_decode(xxoo.string),'utf-8');
		saveimage(imgurl)

def get_page(url):
	headers = {
         'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
         'Host': 'jandan.net'
     }
	html = requests.get(url, headers=headers).text
	soup=BeautifulSoup(html,'html.parser')
	pages=soup.find_all('span',{'class':'current-comment-page'})
	# for page in(pages):
	# 	print(page.text)
	page=pages[1].text
	return page[1:3]



num=int(get_page(url))
#print(num)
num1=num-1
num2=num-2

#get page one
get_urls(url)

#get page two

urlone=url+"/page-"+str(num1)+"#comments"
get_urls(urlone)

#get page three
urltwo=url+"/page-"+str(num2)+"#comments"
get_urls(urltwo)
