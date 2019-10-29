# encoding: utf-8
"""
@project = javbus_crawler
@file = downloadtest
@author = ThinkPad
@create_time = 2019-10-2921:55
"""
import requests
import re
from bs4 import BeautifulSoup

url = 'https://www.dmmsee.icu/EIKI-087'
homeres = requests.get(url)
soup = BeautifulSoup(homeres.text)

paramsElems = soup.find_all('script')[8]
text = paramsElems.text
gid = text[12:24]
reqUrl = 'https://www.dmmsee.icu/ajax/uncledatoolsbyajax.php'
user_agent = 'Mozilla / 5.0 (Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, ' \
             'like Gecko) Chrome / 64.0.3282.140 Safari / 537.36 Edge / 18.17763 '
header = {'User-agent': user_agent, 'referer': url}

payload = {'gid': gid, 'uc': 0}

tableRes = requests.get(reqUrl, params=payload, headers=header, timeout=20)
tableRes.raise_for_status()

magnetSoup = BeautifulSoup(tableRes.text, 'html.parser')
magnetElems = magnetSoup.select('a[style="color:#333"]')
m = 0
pattern = r'\r|\n| |\t'
# links = []

while m < len(magnetElems):
    magnetLink = magnetElems[m].get('href')
    movieFile = re.sub(pattern, '', magnetElems[m].text)
    m += 1
    movieSize = re.sub(pattern, '', magnetElems[m].text)
    m += 1
    movieDate = re.sub(pattern, '', magnetElems[m].text)
    print(movieDate)
    if movieDate == '0000-00-00':
        movieDate = '1900-01-01'
    m += 1
    print(m, 'movieFile:{} movieSize{} movieDate{}\n'.format(movieFile, movieSize, movieDate))
