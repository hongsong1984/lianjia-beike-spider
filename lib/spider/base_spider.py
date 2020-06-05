#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 爬虫基类
# 爬虫名常量，用来设置爬取哪个站点
import copy

import threading
from conf.config import SPIDER_NAME
from lib.zone.area import get_areas
from lib.zone.city import lianjia_cities, beike_cities
from lib.utility.date import *
import lib.utility.version
import random
from conf.const import SZ_FUTIAN_DISTRICT_AREAS, SZ_NANSHAN_AREAS, SZ_NANSHAN_DISTRICT_AREAS, SZ_FUTIAN_AREAS, \
    LIANJIA_SPIDER, BEIKE_SPIDER
from lib.utility.path import *
from lib.zone.district import get_districts
from lib.zone.district import area_dict

thread_pool_size = 1

# 防止爬虫被禁，随机延迟设定
# 如果不想delay，就设定False，
# 具体时间可以修改random_delay()，由于多线程，建议数值大于10
RANDOM_DELAY = False


class BaseSpider(object):
    @staticmethod
    def random_delay():
        if RANDOM_DELAY:
            time.sleep(random.randint(0, 16))

    def __init__(self, name):
        self.name = name
        if self.name == LIANJIA_SPIDER:
            self.cities = lianjia_cities
        elif self.name == BEIKE_SPIDER:
            self.cities = beike_cities
        else:
            self.cities = None
        # 准备日期信息，爬到的数据存放到日期相关文件夹下
        self.date_string = get_date_string()
        print('Today date is: %s' % self.date_string)

        self.total_num = 0  # 总的小区个数，用于统计
        print("Target site is {0}.com".format(SPIDER_NAME))
        self.mutex = threading.Lock()  # 创建锁

    def create_prompt_text(self):
        """
        根据已有城市中英文对照表拼接选择提示信息
        :return: 拼接好的字串
        """
        city_info = list()
        count = 0
        for en_name, ch_name in self.cities.items():
            count += 1
            city_info.append(en_name)
            city_info.append(": ")
            city_info.append(ch_name)
            if count % 4 == 0:
                city_info.append("\n")
            else:
                city_info.append(", ")
        return 'Which city do you want to crawl?\n' + ''.join(city_info)

    def get_chinese_city(self, en):
        """
        拼音拼音名转中文城市名
        :param en: 拼音
        :return: 中文
        """
        return self.cities.get(en, None)

    def init_global_params(self, type, city, district=None):
        global area_dict
        print(id(area_dict))

        self.today_path = create_date_path("{0}/{1}".format(SPIDER_NAME, type), city, self.date_string)

        # 获得城市有多少区列表, district: 区县
        districts = get_districts(city)
        print('City: {0}'.format(city))
        print('Districts: {0}'.format(districts))

        # 获得每个区的板块, area: 板块
        if city == r'sz' and district==r'futianqu':
            areas = SZ_FUTIAN_AREAS
            for k,v in SZ_FUTIAN_DISTRICT_AREAS.items():
                area_dict[k] = v
        elif city == r'sz' and district==r'nanshanqu':
            areas = SZ_NANSHAN_AREAS
            for k,v in SZ_NANSHAN_DISTRICT_AREAS.items():
                area_dict[k] = v
        else:
            areas = list()
            for district in districts:
                areas_of_district = get_areas(city, district)
                print('{0}: Area list:  {1}'.format(district, areas_of_district))
                # 用list的extend方法,L1.extend(L2)，该方法将参数L2的全部元素添加到L1的尾部
                areas.extend(areas_of_district)
                # 使用一个字典来存储区县和板块的对应关系, 例如{'beicai': 'pudongxinqu', }
                for area in areas_of_district:
                    area_dict[area] = district
        print("Area:", areas)
        print("District and areas:", area_dict)

        return areas