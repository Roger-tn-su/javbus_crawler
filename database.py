import pymysql
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
        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='19820612',
                               database='movie1026',
                               use_unicode=True,
                               charset='utf8')
        c = conn.cursor()

        with conn:
            return db_func(c, *args, **kwargs)

    return wrapper


@db_connection_movies
def init(c):
    # Now Handle by decorator
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()

    c.execute(""" CREATE TABLE IF NOT EXISTS `movies` (`m_id` INT AUTO_INCREMENT PRIMARY KEY ,
                                                        `avNum` VARCHAR(40) UNIQUE , 
                                                        `title` TEXT, 
                                                        `coverImgUrl` TEXT, 
                                                        `thumbImgUrl` TEXT,
                                                        `release` DATE,
                                                        `length` INTEGER,
                                                        `director` TEXT,
                                                        `producer` TEXT,
                                                        `publisher` TEXT)
                                                        ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;""")
    c.execute(""" CREATE TABLE IF NOT EXISTS `stars` (`s_id` INT AUTO_INCREMENT PRIMARY KEY ,
                                                    `starID` VARCHAR(40) UNIQUE , 
                                                    `name` TEXT, 
                                                    `birthday` DATE,
                                                    `age` INTEGER,
                                                    `height` INTEGER,
                                                    `cups` TEXT,
                                                    `bust` INTEGER,
                                                    `waist` INTEGER,
                                                    `hip` INTEGER,
                                                    `birthplace` TEXT,
                                                    `hobby` TEXT)
                                                    ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;""")
    c.execute(""" CREATE TABLE IF NOT EXISTS `genre` (`g_id` INT AUTO_INCREMENT PRIMARY KEY ,
                                                    `genreID` VARCHAR(40) UNIQUE ,
                                                    `genreName` TEXT,
                                                    `category` TEXT)
                                                     ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;""")
    c.execute(""" CREATE TABLE IF NOT EXISTS `magnets` (`ma_id` INT AUTO_INCREMENT PRIMARY KEY,
                                                        `avNum` VARCHAR(40), 
                                                        `url` TEXT,
                                                        `filename` TEXT,
                                                        `size` TEXT,
                                                        `addTime` DATE,
                                                        FOREIGN KEY(`avNum`) 
                                                        REFERENCES movies(`avNum`))
                                                        ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;""")
    c.execute(""" CREATE TABLE IF NOT EXISTS `images` (`i_id` INT AUTO_INCREMENT PRIMARY KEY ,
                                                    `avNum` VARCHAR(40), 
                                                    `imgUrl` TEXT,
                                                    FOREIGN KEY (avNum) REFERENCES movies(`avNum`)
                                                    )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;""")
    c.execute(""" CREATE TABLE IF NOT EXISTS `m_s` (`m_s_id` INT AUTO_INCREMENT PRIMARY KEY ,
                                                    `avNum` VARCHAR(40), 
                                                    `starID` VARCHAR(255),
                                                    FOREIGN KEY (avNum) REFERENCES movies(`avNum`),
                                                    FOREIGN KEY (starID) REFERENCES stars(`starID`),
                                                    UNIQUE(avNum, starID))
                                                    ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;""")
    c.execute(""" CREATE TABLE IF NOT EXISTS `m_g` (`m_g_id` INT AUTO_INCREMENT PRIMARY KEY ,
                                                    `avNum` VARCHAR(40), 
                                                    `genreID` VARCHAR(40), 
                                                    FOREIGN KEY (avNum) REFERENCES movies(avNum),
                                                    FOREIGN KEY (genreID) REFERENCES genre(genreID),
                                                    UNIQUE(avNum, genreID))
                                                    ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;""")


@db_connection_movies
def insert_movie(c, movie):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()

    # with conn:
    c.execute("REPLACE INTO `movies` (`avNum`, `title`, `coverImgUrl`, `thumbImgUrl`, `release`, "
              "`length`, `director`, `producer`, `publisher`) VALUES (%s, %s, %s, %s, %s, %s, %s, "
              "%s, %s) ",
              (movie.avNum,
               movie.title,
               movie.cover_img,
               movie.thumb_img,
               movie.release_date,
               movie.length,
               movie.director,
               movie.producer,
               movie.publisher))


@db_connection_movies
def insert_star(c, star):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()
    #
    # with conn:
    c.execute(
        "REPLACE INTO `stars`  (`starID`, `name`, `birthday`, `age`, `height`, `cups`, "
        "`bust`, `waist`, `hip`, `birthplace`, `hobby`)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, "
        "%s, %s, %s)", 
        (star.starID,
         star.name,
         star.birthday,
         star.age,
         star.height,
         star.cups,
         star.bust,
         star.waist,
         star.hip,
         star.birthplace,
         star.hobby))


@db_connection_movies
def insert_genre(c, genre):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()
    #
    # with conn:
    c.execute(
        "INSERT INTO `genre` (`genreID`, `genreName`, `category`) VALUES (%s, %s, %s) ",
        (genre.genreID,
         genre.genreName,
         genre.category))


@db_connection_movies
def insert_magnet(c, link):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()
    #
    # with conn:
    c.execute("INSERT INTO `magnets` (`avNum`, `url`, `filename`, `size`, `addTime`) VALUES "
              "(%s, %s, %s, %s, %s)",
              (link.avNum,
               link.url,
               link.filename,
               link.size,
               link.addTime))


@db_connection_movies
def insert_img(c, img, num):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()
    #
    # with conn:
    c.execute("INSERT INTO `images` (`avNum`, `imgUrl`) VALUES (%s, %s) ",
              (num,
               img))


@db_connection_movies
def insert_m_s(c, num, sid):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()
    #
    # with conn:
    c.execute("INSERT INTO `m_s` (`avNum`, `starID`) VALUES (%s, %s)",
              (num,
               sid))


@db_connection_movies
def insert_m_g(c, num, gid):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()
    #
    # with conn:
    c.execute("INSERT INTO `m_g` (`avNum`, `genreID`) VALUES (%s, %s)",
              (num,
               gid))


@db_connection_movies
def check_existence(c, av_num):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()
    #
    # with conn:
    c.execute("SELECT 1 FROM movies WHERE avNum=%s",
              av_num)

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
    c.execute("SELECT avNum FROM magnets WHERE avNum=%s", av_num)
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
    c.execute("SELECT * FROM stars WHERE starID=%s", star_id)
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
    c.execute("SELECT * FROM genre WHERE genreID=%s", genre_id)
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
    star_1 = Star('None', 'None', '1982-06-12', 0, 0, '', 0, 0, 0, '', '')
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
