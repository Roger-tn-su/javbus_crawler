# encoding: utf-8
"""
@project = javbus_crawler
@file = mysqltest
@author = ThinkPad
@create_time = 2019-10-2620:14
"""

import pymysql
from object_prototye import Movie
import datetime

conn = pymysql.connect(host='localhost',user='root',password='19820612', database='test',charset='utf8mb4')
# 创建游标
c = conn.cursor()

c.execute(""" CREATE TABLE IF NOT EXISTS `movies` (`m_id` INT AUTO_INCREMENT PRIMARY KEY ,
                                                    `avNum` VARCHAR(40) , 
                                                    `title` TEXT, 
                                                    `coverImgUrl` TEXT, 
                                                    `release` DATE,
                                                    `length` INTEGER,
                                                    `director` TEXT,
                                                    `producer` TEXT,
                                                    `publisher` TEXT,
                                                    UNIQUE(`avNum`)                                               
                                                )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                                                """)

c.execute(""" CREATE TABLE IF NOT EXISTS `magnets` (`magnetsID` INT AUTO_INCREMENT PRIMARY KEY,
                                                    `avNum` VARCHAR(40) , 
                                                    `url` TEXT,
                                                    `filename` TEXT,
                                                    `size` TEXT,
                                                    `addTime` DATE,
                                                    FOREIGN KEY(`avNum`) REFERENCES movies(avNum))
                                                    ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;""")

m = Movie('test2','test','test',datetime.date.today(),124,'test','test','test')
c.execute("INSERT INTO `movies`(`avNum`, `title`, `coverImgUrl`, `release`, "
          "`length`, `director`, `producer`, `publisher`) VALUES (%s, %s, %s, %s, "
          "%s, %s, %s, %s)",
          (m.avNum,
           m.title,
           m.cover_img,
           m.release_date,
           m.length,
           m.director,
           m.producer,
           m.publisher))
conn.commit()
c.close()
conn.close()




