#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 爬取二手房数据的爬虫派生类

import re
import threadpool
from bs4 import BeautifulSoup
from conf.const import SZ_FUTIAN_DISTRICT_AREAS, SZ_NANSHAN_AREAS, SZ_NANSHAN_DISTRICT_AREAS, HOUSE_DETAIL_INFO
from lib.item.ershou import *
from lib.zone.city import get_city
from lib.spider.base_spider import *
from lib.utility.date import *
from lib.utility.path import *
from lib.zone.area import *
from lib.utility.log import *
import lib.utility.version


class ErShouSpider(BaseSpider):
    def collect_area_ershou_data(self, city_name, area_name, fmt="csv"):
        """
        对于每个板块,获得这个板块下所有二手房的信息
        并且将这些信息写入文件保存
        :param city_name: 城市
        :param area_name: 板块
        :param fmt: 保存文件格式
        :return: None
        """
        district_name = area_dict.get(area_name, "")
        csv_file = self.today_path + "/{0}_{1}.csv".format(district_name, area_name)
        with open(csv_file, "w", encoding='utf-8-sig') as f:
            # 开始获得需要的板块数据
            ershous = self.get_area_ershou_info(city_name, area_name)
            # 锁定，多线程读写
            if self.mutex.acquire(1):
                self.total_num += len(ershous)
                # 释放
                self.mutex.release()
            if fmt == "csv":
                for ershou in ershous:
                    # print(date_string + "," + xiaoqu.text())
                    f.write(self.date_string + "," + ershou.text() + "\n")
        print("Finish crawl area: " + area_name + ", save data to : " + csv_file)

    @staticmethod
    def get_area_ershou_info(city_name, area_name):
        """
        通过爬取页面获得城市指定版块的二手房信息
        :param city_name: 城市
        :param area_name: 版块
        :return: 二手房数据列表
        """
        total_page = 1
        district_name = area_dict.get(area_name, "")
        # 中文区县
        chinese_district = get_chinese_district(district_name)
        # 中文版块
        chinese_area = get_chinese_area(area_name)

        ershou_list = list()
        page = 'http://{0}.{1}.com/ershoufang/{2}/'.format(city_name, SPIDER_NAME, area_name)
        print(page)  # 打印版块页面地址
        headers = create_headers()
        response = requests.get(page, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得总的页数，通过查找总页码的元素信息
        try:
            page_box = soup.find_all('div', class_='page-box')[0]
            matches = re.search('.*"totalPage":(\d+),.*', str(page_box))
            total_page = int(matches.group(1))
        except Exception as e:
            print("\tWarning: only find one page for {0}".format(area_name))
            print(e)

        # 从第一页开始,一直遍历到最后一页
        for num in range(1, total_page + 1):
            page = 'http://{0}.{1}.com/ershoufang/{2}/pg{3}'.format(city_name, SPIDER_NAME, area_name, num)
            print(page)  # 打印每一页的地址
            headers = create_headers()
            BaseSpider.random_delay()
            response = requests.get(page, timeout=10, headers=headers)
            html = response.content
            soup = BeautifulSoup(html, "lxml")

            # 获得有小区信息的panel
            house_elements = soup.find_all('li', class_="clear")
            for house_elem in house_elements:
                price = house_elem.find('div', class_="totalPrice")
                name = house_elem.find('div', class_='title')
                house_name = house_elem.find('div', class_='positionInfo')
                # desc = house_elem.find('div', class_="houseInfo")
                follow_info = house_elem.find('div', class_="followInfo")
                # pic = house_elem.find('a', class_="img").find('img', class_="lj-lazy")

                # 继续清理数据
                house_name = house_name.text.replace("\n", "")
                price = price.text.strip()
                follow_info = follow_info.text.replace("\n", "")
                follow_info = follow_info.split(r'/')

                followers = None
                open_time = None

                if follow_info:
                    followers = follow_info[0].strip()
                    open_time = follow_info[1].strip()
                # desc = desc.text.replace("\n", "").strip()
                # pic = pic.get('data-original').strip()
                # print(pic)


                # 房源详细信息：住宅名称、价格、单价、户型、朝向、面积，楼层，户型结构，建筑类型，建筑结构，装修情况，梯户比例
                # 挂牌时间，交易权数， 上次交易， 房屋用途， 房屋年限， 产权所属，抵押信息，房本条件，房协编码
                house_a_href = name.find('a', href=True)
                house_a_href = house_a_href['href']

                niandai, house_base_dict = ErShouSpider.get_house_detail_info(house_a_href)
                # 作为对象保存
                ershou = ErShou(chinese_district, chinese_area, house_name, price, niandai, followers, open_time, house_base_dict)
                ershou_list.append(ershou)
        return ershou_list

    def start(self, city, district= None):
        # city = get_city()
        areas = self.init_global_params('ershou', city, district)

        t1 = time.time()  # 开始计时


        # 准备线程池用到的参数
        nones = [None for i in range(len(areas))]
        city_list = [city for i in range(len(areas))]
        args = zip(zip(city_list, areas), nones)
        # areas = areas[0: 1]   # For debugging

        # 针对每个板块写一个文件,启动一个线程来操作
        pool_size = thread_pool_size
        pool = threadpool.ThreadPool(pool_size)
        my_requests = threadpool.makeRequests(self.collect_area_ershou_data, args)
        [pool.putRequest(req) for req in my_requests]
        pool.wait()
        pool.dismissWorkers(pool_size, do_join=True)  # 完成后退出

        # 计时结束，统计结果
        t2 = time.time()
        print("Total crawl {0} areas.".format(len(areas)))
        print("Total cost {0} second to crawl {1} data items.".format(t2 - t1, self.total_num))


    @staticmethod
    def get_house_detail_info(a_href):
        house_base_dict = {}
        # 初始化dict，防止某些房子信息字段缺失，导致输出列错误。
        for key in HOUSE_DETAIL_INFO:
            house_base_dict[key] = r''

        niandai =None

        headers = create_headers()
        BaseSpider.random_delay()
        response = requests.get(a_href, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得有小区信息的panel
        house_info = soup.find('div', class_="houseInfo")

        for info in [r'room', r'type', r'area']:
            try:
                sub_node = house_info.find('div', class_=info)
                main_info = sub_node.find('div', class_="mainInfo")
                sub_info = sub_node.find('div', class_="subInfo")
            except Exception as e:
                print('error, house_info:', a_href)

            if info == r'room':
                fangwuhuxing = None if not main_info else main_info.text.strip()
                louceng = None if not sub_info else sub_info.text.strip()
            elif info == r'type':
                chaoxiang = None if not main_info else main_info.text.strip()
                huxingjiegou = None if not sub_info else sub_info.text.strip()
            elif info == r'area':
                mianji = None if not main_info else main_info.text.strip()
                niandai = None if not sub_info else sub_info.text.strip()
                niandai = None if not niandai else niandai.split(r'/')[0]
            else:
                print('error:', info)

        # 获取房源基本信息
        house_div_base = soup.find('div', class_="introContent")
        house_base_items = house_div_base.find_all('li')

        for house_info_item in house_base_items:
            item_name = house_info_item.find('span', class_="label")

            if type(house_info_item.contents[1]) == type(house_info_item): # 'bs4.element.Tag'
                item_content = house_info_item.contents[1].text.strip()
            else:
                item_content = house_info_item.contents[1].strip()
                item_content = item_content.replace(",", "|");

            if item_name:
                item_name = item_name.text.strip()
                # 额外的key不收集，省的列出现错位
                if item_name in HOUSE_DETAIL_INFO:
                    house_base_dict[item_name] = item_content
                else:
                    print('warn, exart item', item_name)
            else:
                print('error, house_info_item', house_info_item)

        return niandai, house_base_dict


if __name__ == '__main__':
    spider = ErShouSpider(SPIDER_NAME)
    spider.start(r'sz', r'nanshanqu')
