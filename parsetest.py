# encoding: utf-8
"""
@project = javbus_crawler
@file = parsetest
@author = ThinkPad
@create_time = 2019-10-2819:48
"""

import parsertest
import database

link_url = 'https://www.dmmsee.icu/genre/hd/3'
av_num = 'AVOP-144'
soup = parsertest.get_link_soup(link_url)
# star_id_list = parsertest.get_starID_list(soup)
# for s in star_id_list:
#     print('enter')
#     if database.check_stars(s[0]):
#         continue # database.insert_m_s(av_num, s[0])
#     else:
#         p = parsertest.get_star(s)
#         database.insert_star(p)
#         # database.insert_m_s(av_num, s[0])
url_elements = soup.select('a[class="movie-box"]')

# url_list = []

for u in url_elements:
    p = [u['href'], u.img['src']]
    print(p)
