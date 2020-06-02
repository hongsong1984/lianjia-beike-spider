#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 小区信息的数据结构


class XiaoQu(object):
    def __init__(self, district, area, name, price, on_sale, age, deal, rent, layout,
                 type, fee, property_company, builder, total_block, total_house):
        self.district = district
        self.area = area
        self.price = price
        self.name = name
        self.on_sale = on_sale
        self.age = r'' if not age else age
        self.deal = r'' if not deal else deal
        self.rent = r'' if not rent else rent
        self.layout = r'' if not layout else layout
        self.type = r'' if not type else type
        self.fee = r'' if not fee else fee
        self.property_company = r'' if not property_company else property_company
        self.builder = r'' if not builder else builder
        self.total_block = r'' if not total_block else total_block
        self.total_house = r'' if not total_house else total_house

    def text(self):
        return self.district + "," + \
                self.area + "," + \
                self.name + "," + \
                self.price + "," + \
                self.on_sale + "," + \
                self.age + "," + \
                self.deal + "," + \
                self.rent + "," + \
                self.layout + "," + \
                self.type + "," + \
                self.fee + "," + \
                self.property_company + "," + \
                self.builder + "," + \
                self.total_block + "," + \
                self.total_house
