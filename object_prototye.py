
class Movie:
    """ class for each movie in javbus website"""

    def __init__(self, av_num, title, cover_imgurl, thumb_imgurl, date, length, director, producer, publisher):
        self._avNum = av_num
        self._title = title
        self._cover_img = cover_imgurl
        self._thumb_img = thumb_imgurl
        self._release_date = date
        self._length = length
        self._director = director
        self._producer = producer
        self._publisher = publisher

    @property
    def avNum(self):
        return self._avNum

    @property
    def title(self):
        return self._title

    @property
    def cover_img(self):
        return self._cover_img

    @property
    def thumb_img(self):
        return self._thumb_img

    @property
    def release_date(self):
        return self._release_date

    @property
    def length(self):
        return self._length

    @property
    def director(self):
        return self._director

    @property
    def producer(self):
        return self._producer

    @property
    def publisher(self):
        return self._publisher

    def __repr__(self):
        return '{} {} {} {} {} {} {} {}'.format(self._avNum, self._title, self._cover_img,
                                                self._thumb_img, self._release_date, self._length,
                                                self._director, self._producer, self._publisher)


class Star:
    def __init__(self,star_id, name, birthday, age, height, cups, bust, waist, hip, birthplace, hobby,):
        self._starID = star_id
        self._name = name
        self._birthday = birthday
        self._age = age
        self._height = height
        self._cups = cups
        self._bust = bust
        self._waist = waist
        self._hip = hip
        self._birthplace = birthplace
        self._hobby = hobby

    @property
    def starID(self):
        return self._starID

    @property
    def name(self):
        return self._name

    @property
    def birthday(self):
        return self._birthday

    @property
    def age(self):
        return self._age

    @property
    def height(self):
        return self._height

    @property
    def cups(self):
        return self._cups

    @property
    def bust(self):
        return  self._bust

    @property
    def waist(self):
        return self._waist

    @property
    def hip(self):
        return self._hip

    @property
    def birthplace(self):
        return self._birthplace

    @property
    def hobby(self):
        return self._hobby

    def __repr__(self):
        return '{} {} {} {} {} {} {} {} {} {} {}'.format(self._starID, self._name, self._birthday,
                                                   self.age, self._height, self.cups,
                                                   self._bust, self._waist, self._hip,
                                                   self._birthplace, self._hobby)



class Genre:
    def __init__(self, genre_id, genre_name, category):
        self._genreID = genre_id
        self._genreName = genre_name
        self._category = category

    @property
    def genreID(self):
        return self._genreID

    @property
    def genreName(self):
        return self._genreName

    @property
    def category(self):
        return self._category

    def __repr__(self):
        return '{} {} {}'.format(self._genreID, self._genreName, self._category)


class Link:
    """ Class for magnet link"""

    def __init__(self, avNum, magnet, filename, size, add_time):
        self._avNum = avNum
        self._magnet = magnet
        self._filename = filename
        self._size = size
        self._addTime = add_time

    @property
    def size(self):
        return self._size

    @property
    def url(self):
        return self._magnet

    @property
    def avNum(self):
        return self._avNum

    @property
    def filename(self):
        return self._filename

    @property
    def addTime(self):
        return self._addTime

    def __repr__(self):
        return '{} {} {} {} {}'.format(self._avNum, self._magnet, self._filename, self._size,
                                       self._addTime)


class Counter:
    """ Class for counter"""
    def __init__(self):
        self._parsing_time = 0
        self._page_skip = 0
        self._movie_skip = 0

    @property
    def parsing_time(self):
        return self._parsing_time

    @property
    def page_skip(self):
        return self._page_skip

    @property
    def movie_skip(self):
        return self._movie_skip

    def reset_movie_skip(self):
        self._movie_skip = 0

    def increment_movie_skip(self):
        self._movie_skip += 1

    def increment_page_skip(self):
        self._page_skip += 1

    def increment_parse(self):
        self._parsing_time += 1
