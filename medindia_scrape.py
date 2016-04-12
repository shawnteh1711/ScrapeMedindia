'''
A python script to scrape medindia.net and get all the details available of each drug and export them as a json.
'''


#All the Required imports

from lxml import etree
import requests
import time
import urllib2
import mechanize
from bs4 import BeautifulSoup
import re
import string
import json

alpha='a' #starting with the first alphabet
json_data={} #A dictionary to hold the data as a json

for i in range(26): #looping from 'a' to 'z'

	url='http://www.medindia.net/drug-price/index.asp?alpha='+str(chr(ord('a')+i)) # the url containing the link to all drugs ordered by alphabet

	page=urllib2.urlopen(url)
	time.sleep(5)
	html=page.read()
	tree=etree.HTML(html)
	for drug_no in range(2,101):  #each page contains 99 drugs
		
		try:
			xpath_addr='//tr['+str(drug_no)+']/td[2]/a/@href' # the xpath to get drug link
			link=tree.xpath(xpath_addr)
			link=link[0] # getting the link of the drug page
			xpath_addr='//tr['+str(drug_no)+']/td[2]/a/text()' # the xpath to get drug name
			drug_name=tree.xpath(xpath_addr)
			drug_name=drug_name[0]
			regex=re.compile(r'[\n\r\t]') 
			br=mechanize.Browser()
			br.set_handle_robots(False)
			br.addheaders = [('User-agent', 'Chrome')]
			htmltext=br.open(link).read() #mechanize to open the link and read
			soup = BeautifulSoup(htmltext) 
			row1=""
			row2=[]
			row3=[]
			i=0
			for row in soup.findAll('div',attrs={'class':'report-content'}):
					row1=row1+row.text
					row2=row.text.split(':')

			row3=re.findall(r'\n.*:',row1)

			row4=[]
			i=len(row3)
			str1=""
			json1={}

			for r in range(i):
				if r!=(i-1):
					beg=row1.find(row3[r])
					end=row1.find(row3[r+1])
				
					str1=row1[beg:end]
					beg=str1.find(':')
					
					str1=str1[beg+1:]
					
				else:
					beg=row1.find(row3[r])
				
					str1=row1[beg:]
					beg=str1.find(':')
					
					str1=str1[beg+1:]
				
				lst=re.findall(r'\w+\s',str1)
				str2=''.join(lst)
				lst1=re.findall(r'\w+\s',row3[r])
				str3=''.join(lst1)
				
				json1[str3]=str2

			json_data[drug_name]=json1

		except:
			pass
		with open('data.txt', 'w') as outfile: #outputting the data as a json to a textfile
			json.dump(json_data, outfile)

