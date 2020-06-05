#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 二手房信息的数据结构


class ChengJiao(object):
    def __init__(self, district, area, name, date, price, uni_price, deal_data_dict, deal_history_data):
        self.district = district
        self.area = area
        self.name = name
        self.date = date
        self.price = price
        self.uni_price = uni_price
        self.deal_data_dict = deal_data_dict
        self.deal_history_data = deal_history_data

    def text(self):
        deal_info = ''
        for item in self.deal_data_dict:
            deal_info += self.deal_data_dict[item] + ","

        deal_history = ''.join(self.deal_history_data)

        return self.district + "," + \
                self.area + "," + \
                self.name + "," + \
                self.date + "," + \
                self.price + "," + \
                self.uni_price + "," + \
                deal_info + \
                deal_history
