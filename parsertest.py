#! /usr/bin/env python3

import bs4
import requests
from object_prototye import Movie, Link, Star, Genre
import crawler
import os
import re
import database


def get_main_page_soup(home_url):
    """ parse main page soup"""

    # request to javbus
    res = requests.get(home_url)
    res.raise_for_status()

    # init beautiful soup
    soup = bs4.BeautifulSoup(res.text, 'lxml')

    return soup


def get_next_page_url(soup):
    """ Get next page url from main page soup"""

    next_page_elements = soup.select('a[id="next"]')

    if len(next_page_elements) < 1:
        # reach the last page
        return False
    else:
        next_page = 'https://www.dmmsee.icu/' + next_page_elements[0]['href']

    return next_page


def get_movie_page_list(soup):
    """ Get view page link list form main page soup"""

    # select all movie box
    url_elements = soup.select('a[class="movie-box"]')

    # url_list = []

    for u in url_elements:
        yield u['href']
        # url_list.append(u['href'])

    # print the number of movies in this page
    # print('项目数：' + str(len(url_list)))

    # return url_list


def get_link_soup(link):
    """ get the soup of given link"""
    viewPageRes = requests.get(link)
    viewPageRes.raise_for_status()

    # make soup of view page
    viewPageSoup = bs4.BeautifulSoup(viewPageRes.text, 'html.parser')

    return viewPageSoup


def get_av_num(link):
    """ get av num"""

    av_num = link.split('/')[-1]

    return av_num


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
    if dateElems is not None:
        date = dateElems.next_sibling[1:]
    else:
        date = ''

    # get movie length
    lengthElems = soup.find('span', text='長度:')
    if lengthElems is not None:
        length = int(str(lengthElems.next_sibling).replace('分鐘', '', 1))
    else:
        length = ''

    # get movie director
    directorElems = soup.find('span', text='導演:')
    if directorElems is not None:
        director = directorElems.next_sibling.next_sibling.text
    else:
        director = ''


    producerElems = soup.find('span', text='製作商:')
    if producerElems is not None:
        producer = producerElems.next_sibling.next_sibling.text
    else:
        producer = ''

    publisherElems = soup.find('span', text='發行商:')
    if publisherElems is not None:
        publisher = publisherElems.next_sibling.next_sibling.text
    else:
        publisher = ''

    movie = Movie(avNum,title,cover_img,date,length,director,producer,publisher)

    return movie


def get_star(star_info):
    page_url = 'https://www.dmmsee.icu/star/' + star_info[0]

    res = requests.get(page_url)
    res.raise_for_status()

    # init beautiful soup
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    star_infos = soup.select('div[class="avatar-box"]')[0].find_all('p')

    # init star infos
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
            starHeight = int(re.findall(r'\d+', item[-1])[0])
        elif item[0] == '罩杯':
            starCups = item[-1]
        elif item[0] == '胸圍':
            starBust = int(re.findall(r'\d+', item[-1])[0])
        elif item[0] == '腰圍':
            starWaist = int(re.findall(r'\d+', item[-1])[0])
        elif item[0] == '臀圍':
            starHip = int(re.findall(r'\d+', item[-1])[0])
        elif item[0] == '出生地':
            starBirthPlace = item[-1]
        elif item[0] == '愛好':
            starHobby = item[-1]

    star = Star(starID, starName, starBirthday, starAge, starHeight, starCups, starBust,
                starWaist, starHip, starBirthPlace, starHobby)

    return star


def get_starID_list(soup):
    """ Get star list from view page"""

    # don't get soup too often, the server will rufused request
    # soup = get_link_soup(link)

    # stars = []

    star_elements = soup.select('div[class="star-name"]')
    for s in star_elements:
        p = [s.a['href'].split('/')[-1], s.text]
        #p = database.check_stars(s.a['href'].split('/')[-1])
        yield p
        # stars.append(s.text)

    # return stars

def get_genre_list(soup):
    """ Get star list from view page"""

    # don't get soup too often, the server will rufused request
    # soup = get_link_soup(link)

    # stars = []

    genre_elems = soup.find('p',text='類別:').next_sibling.next_sibling.select(
        'span[class="genre"]')
    for s in genre_elems:
        p = [s.a['href'].split('/')[-1], s.text]
        yield p
        # stars.append(s.text)

    # return stars


def get_genre(genre_info):
    url = 'https://www.dmmsee.icu/genre'
    genre_res = requests.get(url)
    genre_res.raise_for_status()

    # init beautiful soup
    soup = bs4.BeautifulSoup(genre_res.text, 'lxml')
    href = 'https://www.dmmsee.icu/genre/' + genre_info[0]
    elem = soup.find(name='a', attrs={'href': href})
    elem_parent = elem.parent
    p = Genre(genre_info[0], genre_info[1], elem_parent.previous_sibling.previous_sibling.text)
    return p

def get_sample_img_list(soup):
    """ Get sample images from view page"""

    # don't get soup too often, the server will rufused request
    # soup = get_link_soup(link)

    # sampleImgs = []

    sampleImgElems = soup.select('a[class="sample-box"]')

    for n in sampleImgElems:
        yield n['href']
        # sampleImgs.append(n['href'])

    # return sampleImgs


def get_download_link(soup, home_url, avNum):
    """ get download link"""

    # don't get soup too often, the server will rufused request
    # soup = get_link_soup(link)

    paramsElems = soup.find_all('script')[8]
    text = paramsElems.text
    gid = text[12:24]
    reqUrl = 'https://www.dmmsee.icu/ajax/uncledatoolsbyajax.php'
    header = {'referer': home_url}

    payload = {'gid': gid, 'uc': 0}

    tableRes = requests.get(reqUrl, params=payload, headers=header)
    tableRes.raise_for_status()

    magnetSoup = bs4.BeautifulSoup(tableRes.text, 'html.parser')
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
        m += 1
        p = Link(avNum,magnetLink,movieFile,movieSize,movieDate)
        yield p
        # links.append(Link(avNum, magnetLink, movieSize))

    # return links


# function testing
if __name__ == '__main__':
    print('testing')
    entry = 'https://www.dmmsee.icu/'
    tSoup = get_main_page_soup(entry)

    tUrl = get_next_page_url(tSoup)
    print(tUrl)
    tMovList = get_movie_page_list(tSoup)
    print(tMovList)

    l = next(tMovList)

    tLinkSoup = get_link_soup(l)

    tAvNum = get_av_num(l)
    print(tAvNum)
    tMov = get_movie(tLinkSoup, tAvNum)
    print(tMov)
    tStarList = get_starID_list(tLinkSoup)
    print(tStarList)
    for s in tStarList:
        print(s)
    tImgList = get_sample_img_list(tLinkSoup)
    print(tImgList)
    print(next(tImgList))
    tDownLink = get_download_link(tLinkSoup, entry, tAvNum)
    print(tDownLink)
    print(next(tDownLink))

