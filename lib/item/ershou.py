#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 二手房信息的数据结构


class ErShou(object):
    def __init__(self, district, area, name, price, niandai, follow, open_time, house_base_dict):
        self.district = district
        self.area = area
        self.name = name
        self.price = price
        self.niandai = niandai
        self.follow = follow
        self.open_time = open_time
        self.house_base_dict = house_base_dict

    def text(self):
        base_info = ''
        for item in self.house_base_dict:
            base_info += self.house_base_dict[item] + ","
        return self.district + "," + \
                self.area + "," + \
                self.name + "," + \
                self.price + "," + \
                self.follow + "," + \
                self.open_time + "," + \
                base_info + \
                self.niandai
