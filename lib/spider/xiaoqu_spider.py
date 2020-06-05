#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 爬取小区数据的爬虫派生类
import codecs
import csv

import re
import string
import threadpool
from bs4 import BeautifulSoup
from conf.const import SZ_AREAS, SZ_DISTRICT_AREAS, SZ_FUTIAN_DISTRICT_AREAS, SZ_FUTIAN_AREAS, SZ_NANSHAN_AREAS, \
    SZ_NANSHAN_DISTRICT_AREAS
from lib.item.xiaoqu import *
from lib.zone.city import get_city
from lib.spider.base_spider import *
from lib.utility.date import *
from lib.utility.path import *
from lib.zone.area import *
from lib.utility.log import *
import lib.utility.version
import re


class XiaoQuBaseSpider(BaseSpider):
    def collect_area_xiaoqu_data(self, city_name, area_name, fmt="csv"):
        """
        对于每个板块,获得这个板块下所有小区的信息
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
            xqs = self.get_xiaoqu_info(city_name, area_name)
            # 锁定
            if self.mutex.acquire(1):
                self.total_num += len(xqs)
                # 释放
                self.mutex.release()
            if fmt == "csv":
                for xiaoqu in xqs:
                    f.write(self.date_string + "," + xiaoqu.text() + "\n")
        print("Finish crawl area: " + area_name + ", save data to : " + csv_file)
        logger.info("Finish crawl area: " + area_name + ", save data to : " + csv_file)

    @staticmethod
    def get_xiaoqu_info(city, area):
        total_page = 1
        district = area_dict.get(area, "")
        chinese_district = get_chinese_district(district)
        chinese_area = get_chinese_area(area)
        xiaoqu_list = list()
        page = 'http://{0}.{1}.com/xiaoqu/{2}/'.format(city, SPIDER_NAME, area)
        print(page)
        logger.info(page)

        headers = create_headers()
        response = requests.get(page, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得总的页数
        try:
            page_box = soup.find_all('div', class_='page-box')[0]
            matches = re.search('.*"totalPage":(\d+),.*', str(page_box))
            total_page = int(matches.group(1))
        except Exception as e:
            print("\tWarning: only find one page for {0}".format(area))
            print(e)

        # 从第一页开始,一直遍历到最后一页
        for i in range(1, total_page + 1):
            headers = create_headers()
            page = 'http://{0}.{1}.com/xiaoqu/{2}/pg{3}'.format(city, SPIDER_NAME, area, i)
            print(page)  # 打印版块页面地址
            BaseSpider.random_delay()
            response = requests.get(page, timeout=10, headers=headers)
            html = response.content
            soup = BeautifulSoup(html, "lxml")

            # 获得有小区信息的panel
            house_elems = soup.find_all('li', class_="xiaoquListItem")
            for house_elem in house_elems:
                price = house_elem.find('div', class_="totalPrice")
                name = house_elem.find('div', class_='title')
                on_sale = house_elem.find('div', class_="xiaoquListItemSellCount")

                # 增加小区建筑时间、户型和成交套数
                house_info = house_elem.find('div', class_="houseInfo")
                position_info = house_elem.find('div', class_="positionInfo")

                # 小区建筑类型、开发商、物业、物业费、栋数、房屋总数
                house_a_href = name.find('a', class_="maidian-detail", href=True)
                jianzhuleixing, wuyefeiyong, wuyegongsi, kaifashang, loudongzongshu, fangwuzongshu = [None] * 6
                if house_a_href.get_text(strip=True):
                    jianzhuleixing, wuyefeiyong, wuyegongsi, kaifashang, loudongzongshu, fangwuzongshu = XiaoQuBaseSpider.get_xiaoqu_detail_info(house_a_href['href'])

                # 继续清理数据
                price = price.text.strip()
                name = name.text.replace("\n", "")
                on_sale = on_sale.text.replace("\n", "").strip()

                house_info = house_info.text.strip()
                house_info = house_info.replace("\n", "")
                house_infos = house_info.split(r'|')
                huxing = None
                chengjiao = None
                chuzu = None

                for info in house_infos:
                    digital_info = re.findall(r"\d+", info)[-1]
                    if r'户型' in info:
                        huxing = digital_info
                    elif r'成交' in info:
                        chengjiao = digital_info
                    elif r'出租' in info:
                        chuzu = digital_info
                    else:
                        print('house_infos parse error', house_info)

                position_info = position_info.text.strip()
                position_info = position_info.replace("\n", "")
                niandai = re.findall(r"\d+", position_info)
                if niandai:
                    niandai = niandai[-1]
                else:
                    index = position_info.find(r'年建成')
                    niandai = position_info[index-2: index]
                    # print('position_info parse error', position_info)

                # 把在售房源的数字提出来
                on_sale = re.findall(r"\d+", on_sale)
                if on_sale:
                    on_sale = on_sale[0]

                # 作为对象保存
                xiaoqu = XiaoQu(chinese_district, chinese_area, name, price, on_sale,
                                niandai, chengjiao, chuzu, huxing, jianzhuleixing,
                                wuyefeiyong, wuyegongsi, kaifashang, loudongzongshu, fangwuzongshu)
                xiaoqu_list.append(xiaoqu)
        return xiaoqu_list

    @staticmethod
    def get_xiaoqu_detail_info(a_href):
        jianzhuleixing = None
        wuyefeiyong = None
        wuyegongsi = None
        kaifashang = None
        loudongzongshu = None
        fangwuzongshu = None

        headers = create_headers()
        BaseSpider.random_delay()
        response = requests.get(a_href, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得有小区信息的panel
        house_infos = soup.find('div', class_="xiaoquInfo")
        if house_infos:
            house_info_items = house_infos.find_all('div', class_="xiaoquInfoItem")

            for house_info_item in house_info_items:
                item_name = house_info_item.find('span', class_="xiaoquInfoLabel")
                item_content = house_info_item.find('span', class_="xiaoquInfoContent")

                if r'建筑类型' in item_name.text.strip():
                    jianzhuleixing = item_content.text.strip()
                elif r'物业费用' in item_name.text.strip():
                    wuyefeiyong = item_content.text.strip()
                elif r'物业公司' in item_name.text.strip():
                    wuyegongsi = item_content.text.strip()
                    wuyegongsi = wuyegongsi.translate(str.maketrans('', '', string.punctuation))
                elif r'开发商' in item_name.text.strip():
                    kaifashang = item_content.text.strip()
                    kaifashang = kaifashang.translate(str.maketrans('', '', string.punctuation))
                elif r'楼栋总数' in item_name.text.strip():
                    loudongzongshu = item_content.text.strip()
                elif r'房屋总数' in item_name.text.strip():
                    fangwuzongshu = item_content.text.strip()
                else:
                    pass
        else:
            print('error:', a_href)
        return jianzhuleixing, wuyefeiyong, wuyegongsi, kaifashang, loudongzongshu, fangwuzongshu

    def start(self, city, district):
        # city = get_city()

        areas = self.init_global_params('xiaoqu', city, district)
        t1 = time.time()  # 开始计时

        # 准备线程池用到的参数
        nones = [None for i in range(len(areas))]
        city_list = [city for i in range(len(areas))]
        args = zip(zip(city_list, areas), nones)
        # areas = areas[0: 1]

        # 针对每个板块写一个文件,启动一个线程来操作
        pool_size = thread_pool_size
        pool = threadpool.ThreadPool(pool_size)
        my_requests = threadpool.makeRequests(self.collect_area_xiaoqu_data, args)
        [pool.putRequest(req) for req in my_requests]
        pool.wait()
        pool.dismissWorkers(pool_size, do_join=True)  # 完成后退出

        # 计时结束，统计结果
        t2 = time.time()
        print("Total crawl {0} areas.".format(len(areas)))
        print("Total cost {0} second to crawl {1} data items.".format(t2 - t1, self.total_num))


if __name__ == "__main__":
    # urls = get_xiaoqu_area_urls()
    # print urls
    spider = XiaoQuBaseSpider("ke")
    # spider.init_global_params(r'sz')
    # spider.collect_area_xiaoqu_data('sz', 'huaqiangnan')
    spider.start(r'sz', r'nanshanqu')
