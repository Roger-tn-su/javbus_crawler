import sqlite3
from object_prototye import Movie
from object_prototye import Link
from object_prototye import Star
from object_prototye import Genre
import datetime
import os
from bs4 import BeautifulSoup
import requests


def db_connection_movies(db_func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('/javbus_crawler/movies1019.db')
        c = conn.cursor()

        with conn:
            return db_func(c, *args, **kwargs)

    return wrapper


@db_connection_movies
def init(c):
    # Now Handle by decorator
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()

    c.execute(""" CREATE TABLE IF NOT EXISTS movies (avNum TEXT PRIMARY KEY, 
                                                    title TEXT, 
                                                    coverImgUrl TEXT, 
                                                    release DATE,
                                                    length INTEGER,
                                                    director TEXT,
                                                    producer TEXT,
                                                    publisher TEXT)""")
    c.execute(""" CREATE TABLE IF NOT EXISTS stars (starID TEXT PRIMARY KEY, 
                                                    name TEXT, 
                                                    birthday DATE,
                                                    age INTEGER,
                                                    height INTEGER,
                                                    cups TEXT,
                                                    bust INTEGER,
                                                    waist INTEGER,
                                                    hip INTEGER,
                                                    birthplace TEXT,
                                                    hobby TEXT)""")
    c.execute(""" CREATE TABLE IF NOT EXISTS genre (genreID TEXT PRIMARY KEY,
                                                    genreName TEXT,
                                                    category TEXT) """)
    c.execute(""" CREATE TABLE IF NOT EXISTS magnets (avNum TEXT, 
                                                        url TEXT,
                                                        filename TEXT,
                                                        size TEXT,
                                                        addTime DATE,
                                                        FOREIGN KEY(avNum) REFERENCES movies(avNum),
                                                        UNIQUE(avNum, url))""")
    c.execute(""" CREATE TABLE IF NOT EXISTS images (avNum TEXT, 
                                                    imgUrl TEXT,
                                                    FOREIGN KEY (avNum) REFERENCES movies(avNum),
                                                        UNIQUE(avNum, imgUrl))""")
    c.execute(""" CREATE TABLE IF NOT EXISTS m_s (avNum TEXT, 
                                                  starID TEXT,
                                                  FOREIGN KEY (avNum) REFERENCES movies(avNum),
                                                  FOREIGN KEY (starID) REFERENCES stars(starID),
                                                  UNIQUE(avNum, starID))""")
    c.execute(""" CREATE TABLE IF NOT EXISTS m_g (avNum TEXT, 
                                                  genreID TEXT, 
                                                  FOREIGN KEY (avNum) REFERENCES movies(avNum),
                                                  FOREIGN KEY (genreID) REFERENCES genre(genreID),
                                                  UNIQUE(avNum, genreID))""")


@db_connection_movies
def insert_movie(c, movie):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()

    # with conn:
    c.execute("INSERT OR REPLACE INTO movies VALUES (:avNum, :title, :coverImgUrl, :release, "
              ":length, :director, :producer, :publisher)",
              {'avNum': movie.avNum,
               'title': movie.title,
               'coverImgUrl': movie.cover_img,
               'release': movie.release_date,
               'length': movie.length,
               'director': movie.director,
               'producer': movie.producer,
               'publisher': movie.publisher})


@db_connection_movies
def insert_star(c, star):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()
    #
    # with conn:
    c.execute(
        "INSERT OR REPLACE INTO stars VALUES (:starID, :name, :birthday, :age, :height, :cups, "
        ":bust, :waist, :hip, :birthplace, :hobby)",
        {'starID': star.starID,
         'name': star.name,
         'birthday': star.birthday,
         'age': star.age,
         'height': star.height,
         'cups': star.cups,
         'bust': star.bust,
         'waist': star.waist,
         'hip': star.hip,
         'birthplace': star.birthplace,
         'hobby': star.hobby})


@db_connection_movies
def insert_genre(c, genre):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()
    #
    # with conn:
    c.execute(
        "INSERT OR REPLACE INTO genre VALUES (:genreID, :genreName, :category)",
        {'genreID': genre.genreID,
         'genreName': genre.genreName,
         'category': genre.category, })


@db_connection_movies
def insert_magnet(c, link):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()
    #
    # with conn:
    c.execute("INSERT OR REPLACE INTO magnets VALUES (:avNum, :url, :filename, :size, :addTime)",
              {'avNum': link.avNum,
               'url': link.url,
               'filename': link.filename,
               'size': link.size,
               'addTime': link.addTime})


@db_connection_movies
def insert_img(c, img, num):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()
    #
    # with conn:
    c.execute("INSERT OR REPLACE INTO images VALUES (:avNum, :name)",
              {'avNum': num,
               'name': img})


@db_connection_movies
def insert_m_s(c, num, sid):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()
    #
    # with conn:
    c.execute("INSERT OR REPLACE INTO m_s VALUES (:avNum, :starID)",
              {'avNum': num,
               'starID': sid})


@db_connection_movies
def insert_m_g(c, num, gid):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()
    #
    # with conn:
    c.execute("INSERT OR REPLACE INTO m_g VALUES (:avNum, :genreID)",
              {'avNum': num,
               'genreID': gid})


@db_connection_movies
def check_existence(c, av_num):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()
    #
    # with conn:
    c.execute("SELECT 1 FROM movies WHERE avNum=:avNum",
              {'avNum': av_num})

    if c.fetchone() is not None:
        print('data exists')
        return True
    else:
        # print('not exists')
        return False


@db_connection_movies
def check_links(c, av_num):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()
    #
    # with conn:
    c.execute("SELECT avNum FROM magnets WHERE avNum=:avNum", {'avNum': av_num})
    if c.fetchone() is not None:
        # print('link exists')
        return True
    else:
        # print('not exists')
        return False


@db_connection_movies
def check_stars(c, star_id):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()
    #
    # with conn:
    c.execute("SELECT * FROM stars WHERE starID=:starID", {'starID': star_id})
    if c.fetchone() is not None:
        # print('star exists')
        return True
    else:
        print('star not exists')
        return False


@db_connection_movies
def check_genres(c, genre_id):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()
    #
    # with conn:
    c.execute("SELECT * FROM genre WHERE genreID=:genreID", {'genreID': genre_id})
    if c.fetchone() is not None:
        # print('genre exists')
        return True
    else:
        print('genre not exists')
        return False


def update_genres(entry_url):
    url = entry_url + 'genre'
    res = requests.get(url)
    res.raise_for_status()

    genresoup = BeautifulSoup(res.text, 'lxml')
    categorys = genresoup.select('div[class="container-fluid pt10"]')
    themes = categorys[0].select('h4')
    i = 0
    for theme in themes:
        # print(theme.text)
        # print(target)
        genreList = theme.next_sibling.next_sibling.select('a')
        # print(genreList)
        # j = 0
        # print(genreList[j]['href'].split('/')[-1])
        for genre in genreList:
            if check_genres(genre['href'].split('/')[-1]) is not True:
                p = Genre(genre['href'].split('/')[-1], genre.text, theme.text)
                print(p)
                insert_genre(p)


if __name__ == '__main__':

    init()
    # mov_1 = Movie('testMovie', 'test', 'test', '2019-06-20', 1, 'test', 'test', 'test')
    star_1 = Star('None', 'None', '', 0, 0, '', 0, 0, 0, '', '')
    genre_1 = Genre('None', 'None', 'None')
    # link_1 = Link('testMovie', 'test', 'test', 'test', datetime.date.today())

    # insert_movie(mov_1)
    insert_star(star_1)
    insert_genre(genre_1)

    entry_url = 'https://www.dmmsee.icu/'
    update_genres(entry_url)
    # insert_magnet(link_1)
    # insert_img('test','testMovie')
    # insert_m_s('testMovie', 'testStar')
    # insert_m_g('testMovie', 'testGenre')
    #
    # check_existence('testMovie')
    # check_stars('testStar')
