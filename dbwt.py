# encoding: utf-8
"""
@project = javbus_crawler
@file = dbwt
@author = ThinkPad
@create_time = 2019-11-0410:52
"""
import database
import re
import os


@database.db_connection_movies
def fetch_thumbimg(c):
    len = c.execute("SELECT `m_id`, `coverImgUrl`, `thumbImgUrl` FROM movie1026.movies")
    records = c.fetchall()
    for record in records:
        # record = records[i]
        # print(type(record))
        if re.match(r'https://pics.javcdn.pw/cover/.+\.jpg',record[1]):
            filename = os.path.basename(record[1]).replace('_b.jpg','')
            thumb = 'https://pics.javcdn.pw/thumb/' + filename + '.jpg'
            c.execute("UPDATE movie1026.movies SET `thumbImgUrl` = %s WHERE m_id = %s",
                      (thumb, record[0]))
        elif re.match(r'https://pics.dmm.co.jp/digital/video/.+\.jpg', record[1]):
            thumb = record[1].replace('pl.jpg', 'ps.jpg')
            c.execute("UPDATE movie1026.movies SET `thumbImgUrl` = %s WHERE m_id = %s",
                      (thumb, record[0]))

    # d = c.fetchone()
    # print(os.path.basename(d[1]))

if __name__ == '__main__':
    fetch_thumbimg()