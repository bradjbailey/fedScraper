## FOMC ADVANCED SEARCH SCRAPER ##

import re
from bs4 import BeautifulSoup
import requests

## pages - from original url, return list of urls to scrape

url = "https://www.fedsearch.org/fomc-docs/search?advanced_search=true&to_month=2&to_year=2022&number=10&from_year=1936&Search=Search&search_precision=All+Words&start=0&text=&sort=Relevance&from_month=3"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")     

## grab number of total results

##found = soup.find(string = "%matched%") ## not working
##print(found)

results = soup.find("h2", class_ = "borderdash")
numResults = re.split("[, \r]", results.string)
print(numResults[-2]) ## should give number of results
totRes = numResults[-2]
totRes = int(totRes)
print(totRes)
print(type(totRes))

## find where 'number=' is in the string, determines entires per page (up to 100)
num = url.find("number=")
listurl = list(url)
## add 0 to the end to change 10 entries per page to 100 per page
## 'number=10' is 9 characters
listurl.insert(num+9, "0")
url = ''.join(listurl)
print(url)

## create list of urls
start = url.find("start=")
## 'start=0' is  7 characters
## want list with start = 0, start = 100, start = 200, etc up to numResults[-2]
numPages = int(totRes/100)
print(numPages)

urlList = [url]
listurl = list(url)

for i in range(1, numPages+1, 1):
    listurl[start+6] = i*100
    urlList.append(''.join(map(str, listurl)))

print(urlList)

## downloader - for each page, download all PDFs and HTML files as raw text

## main - take a url from FOMC adv search and return text data