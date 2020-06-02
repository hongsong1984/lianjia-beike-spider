#!/usr/bin/env python
# coding=utf-8

from lib.spider.xiaoqu_spider import *

import csv

def create_date_path(site, city, date):
    city_path = create_city_path(site, city)
    date_path = city_path + "/" + date
    print(date_path)

if __name__ == "__main__":
    spider = XiaoQuBaseSpider(SPIDER_NAME)
    district_name = r'luohuqu'
    area_name = r'baishida'

    xqs = spider.get_xiaoqu_info(r'sz', r'baishida')

    with open('test.csv', "w", encoding='utf-8-sig') as f:
        for xiaoqu in xqs:
            f.write('2020' + "," + xiaoqu.text() + "\n")

