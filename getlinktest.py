# encoding: utf-8
"""
@project = javbus_crawler
@file = getlinktest
@author = ThinkPad
@create_time = 2019-10-108:35
"""
import requests
from bs4 import BeautifulSoup
import re
from object_prototye import Movie,Star
import datetime


# def get_download_link(soup, home_url):
#     """ get download link"""
#
#     # don't get soup too often, the server will rufused request
#     # soup = get_link_soup(link)
#
#     paramsElems = soup.find_all('script')[8]
#     text = paramsElems.text
#     gid = text[12:24]
#     reqUrl = 'https://www.dmmsee.icu/ajax/uncledatoolsbyajax.php'
#     header = {'referer': home_url}
#
#     payload = {'gid': gid, 'uc': 0}
#
#     tableRes = requests.get(reqUrl, params=payload, headers=header)
#     tableRes.raise_for_status()
#
#     linksoup = BeautifulSoup(tableRes.text, 'html.parser')
#
#     return (linksoup)


#

def get_movie(soup, avNum):
    """ Get movie info from view page"""

    # don't get soup too often, the server will rufuse request
    # soup = get_link_soup(link)

    # get cover and title
    bigImgElems = soup.select('.bigImage img')

    # get title
    title = bigImgElems[0].get('title')

    # get cover image url
    cover_img = bigImgElems[0].get('src')

    # get release date
    dateElems = soup.find('span', text="發行日期:")
    date = dateElems.next_sibling[1:]

    # get movie length
    lengthElems = soup.find('span', text='長度:')
    length = int(str(lengthElems.next_sibling[1:]).replace('分鐘', '', 1))

    # get movie director

    movie = Movie(avNum, title, cover_img, date)

    return movie


# url = 'https://www.dmmsee.icu/star/myq'
# avno = 'RKI-491'
# homeres = requests.get(url)

# test for stars
with open('starres.html',encoding='utf-8') as file_object:
     contents = file_object.read()
homesoup = BeautifulSoup(contents, 'html.parser')
star_infos = homesoup.select('div[class="avatar-box"]')[0].find_all('p')

star_info = ['tyv', '深田えいみ']
# get star info

starID = star_info[0]
starName = star_info[1]
starBirthday = ''
starAge = ''
starHeight = ''
starCups = ''
starBust = ''
starWaist = ''
starHip = ''
starBirthPlace = ''
starHobby = ''

for elem in star_infos:
    item = elem.text.split(': ')
    if item[0] == '生日':
        starBirthday = item[-1]
    elif item[0] == '年齡':
        starAge = item[-1]
    elif item[0] == '身高':
        starHeight = int(re.findall(r'\d+',item[-1])[0])
    elif item[0] == '罩杯':
        starCups = item[-1]
    elif item[0] == '胸圍':
        starBust = int(re.findall(r'\d+',item[-1])[0])
    elif item[0] == '腰圍':
        starWaist = int(re.findall(r'\d+',item[-1])[0])
    elif item[0] == '臀圍':
        starHip = int(re.findall(r'\d+',item[-1])[0])
    elif item[0] == '出生地':
        starBirthPlace = item[-1]
    elif item[0] == '愛好':
        starHobby = item[-1]

star = Star(starID, starName, starBirthday, starAge, starHeight, starCups, starBust,
            starWaist, starHip, starBirthPlace, starHobby)

print(star)


        # starBirthday = star_infos[0].text.split(': ')[-1]
# starAge = star_infos[1].text.split(': ')[-1]
# starHeight = int(re.findall(r'\d+',star_infos[2].text)[0])
# starCups = star_infos[3].text.split(': ')[-1]
# starBust = int(re.findall(r'\d+', star_infos[4].text)[0])
# starWaist = int(re.findall(r'\d+', star_infos[5].text)[0])
# starHip = int(re.findall(r'\d+', star_infos[6].text)[0])
# starBirthPlace = star_infos[7].text.split(': ')[-1]
# starHobby = star_infos[8].text.split(': ')[-1]
#
# star = Star(starID, starName, starBirthday, starAge, starHeight, starCups, starBust, starWaist,
#             starHip, starBirthPlace, starHobby)

print(star)

# test for genre
# soup = get_download_link(homesoup, url)
# elems = soup.select('a[style="color:#333"]')
# for i, item in enumerate(elems):
#     #     # title = re.sub(r' HD$','',item.text)
#     print(i, '  ', item.text, '  ', item.get('href'))


# genreElems = homesoup.find('p',text='類別:').next_sibling.next_sibling.select('span[class="genre"]')


# print(type(genreElems),genreElems)
#
# for i in genreElems:
#     print(i.a['href'].split('/')[-1], ' ', i.text)

# # use genre_id to find category
# url = 'https://www.dmmsee.icu/genre'
# genre_res = requests.get(url)
# genre_res.raise_for_status()
#
# # init beautiful soup
# soup = BeautifulSoup(genre_res.text, 'lxml')
# genre_id = '4v'
# href = 'https://www.dmmsee.icu/genre/' + genre_id
# elem = soup.find(name='a',attrs={'href':href})
# elem_parent = elem.parent
# print(elem_parent.previous_sibling.previous_sibling.text)

