#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 爬取二手房数据的爬虫派生类

import re
import threadpool
from bs4 import BeautifulSoup
from conf.const import DEAL_DETAIL_INFO
from lib.item.chengjiao import ChengJiao
from lib.item.ershou import *
from lib.zone.city import get_city
from lib.spider.base_spider import *
from lib.utility.date import *
from lib.utility.path import *
from lib.zone.area import *
from lib.utility.log import *
import lib.utility.version


class ChengJiaoSpider(BaseSpider):
    def collect_area_chengjiao_data(self, city_name, area_name, fmt="csv"):
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
            chengjiaos = self.get_area_chengjiao_info(city_name, area_name)
            # 锁定，多线程读写
            if self.mutex.acquire(1):
                self.total_num += len(chengjiaos)
                # 释放
                self.mutex.release()
            if fmt == "csv":
                for chengjiao in chengjiaos:
                    # print(date_string + "," + xiaoqu.text())
                    f.write(self.date_string + "," + chengjiao.text() + "\n")
        print("Finish crawl area: " + area_name + ", save data to : " + csv_file)

    @staticmethod
    def get_area_chengjiao_info(city_name, area_name):
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

        chengjiao_list = list()
        page = 'http://{0}.{1}.com/chengjiao/{2}/'.format(city_name, SPIDER_NAME, area_name)
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
            page = 'http://{0}.{1}.com/chengjiao/{2}/pg{3}'.format(city_name, SPIDER_NAME, area_name, num)
            print(page)  # 打印每一页的地址
            headers = create_headers()
            BaseSpider.random_delay()
            response = requests.get(page, timeout=10, headers=headers)
            html = response.content
            soup = BeautifulSoup(html, "lxml")

            # 获得有成交信息的panel
            house_elements = soup.find('ul', class_='listContent')
            house_elements = house_elements.find_all('li')
            for house_elem in house_elements:
                name = house_elem.find('a', class_='CLICKDATA maidian-detail')
                deal_date = house_elem.find('div', class_='dealDate')
                total_price = house_elem.find('div', class_='totalPrice')
                unit_price = house_elem.find('div', class_='unitPrice')

                name = name.text.replace("\n", "").strip()
                name = name.split()[0]
                deal_date = deal_date.text.replace("\n", "").strip()
                total_price = total_price.text.replace("\n", "").strip()
                unit_price = unit_price.text.replace("\n", "").strip()

                house_a_href = house_elem.find('a', class_='maidian-detail', href=True)
                house_a_href = house_a_href['href']

                deal_data_dict, deal_history_data = ChengJiaoSpider.get_deal_detail_info(house_a_href)

                # 作为对象保存
                chengjiao = ChengJiao(chinese_district, chinese_area, name, deal_date, total_price, unit_price,
                                      deal_data_dict, deal_history_data)
                chengjiao_list.append(chengjiao)

        return chengjiao_list

    def start(self, city, district= None):
        # city = get_city()
        areas = self.init_global_params('chengjiao', city, district)
        t1 = time.time()  # 开始计时


        # 准备线程池用到的参数
        nones = [None for i in range(len(areas))]
        city_list = [city for i in range(len(areas))]
        args = zip(zip(city_list, areas), nones)
        # areas = areas[0: 1]   # For debugging

        # 针对每个板块写一个文件,启动一个线程来操作
        pool_size = thread_pool_size
        pool = threadpool.ThreadPool(pool_size)
        my_requests = threadpool.makeRequests(self.collect_area_chengjiao_data, args)
        [pool.putRequest(req) for req in my_requests]
        pool.wait()
        pool.dismissWorkers(pool_size, do_join=True)  # 完成后退出

        # 计时结束，统计结果
        t2 = time.time()
        print("Total crawl {0} areas.".format(len(areas)))
        print("Total cost {0} second to crawl {1} data items.".format(t2 - t1, self.total_num))


    @staticmethod
    def get_deal_detail_info(a_href):
        deal_data_dict = {}
        # 初始化dict，防止某些房子信息字段缺失，导致输出列错误。
        for key in DEAL_DETAIL_INFO:
            deal_data_dict[key] = r''


        headers = create_headers()
        BaseSpider.random_delay()
        response = requests.get(a_href, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得成交信息的panel
        deal_info = soup.find('div', class_="info fr")
        deal_info = deal_info.find('div', class_="msg")
        deal_items = deal_info.find_all('span')

        for item in deal_items:
            try:
                content = item.text.replace("\n", "").strip()
                content = content.split()
                key = content[1]
                value = content[0]

                if key in DEAL_DETAIL_INFO:
                    deal_data_dict[key] = value
                else:
                    print('warn, extra key', key)

            except Exception as e:
                print('error, deal_info:', a_href)


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
                if item_name in DEAL_DETAIL_INFO:
                    deal_data_dict[item_name] = item_content
                else:
                    if item_name == r'供暖方式':
                        pass
                    else:
                        print('warn, exart item', item_name)
            else:
                print('error, house_info_item', house_info_item)


        # 获取历史成交记录
        deal_history = soup.find('div', class_="chengjiao_record")
        deal_history_items = deal_history.find_all('li')

        deal_history_data = []

        for item in deal_history_items:
            record_price = item.find(class_='record_price')
            record_detail = item.find(class_='record_detail')
            record_price = record_price.text.replace("\n", "").strip()
            record_detail = record_detail.text.replace("\n", "").strip()
            if len(record_detail.split(',')) > 1:
                record_uni_price = record_detail.split(',')[0]
                record_deal_date = record_detail.split(',')[1].replace("\n", "").strip()
                deal_history_data.append('{0}|{1}|{2}'.format(record_price, record_uni_price, record_deal_date))

        return deal_data_dict, deal_history_data


if __name__ == '__main__':
    spider = ChengJiaoSpider(SPIDER_NAME)
    spider.start(r'sz', r'futianqu')