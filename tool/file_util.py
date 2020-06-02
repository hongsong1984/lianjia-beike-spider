#!/usr/bin/env python
# coding=utf-8

import os
import pandas as pd
from conf.const import HOUSE_DETAIL_INFO


def read_data(file_name, encoding='utf_8_sig'):
    data = None
    try:
        if file_name.endswith('.csv'):
            data = pd.read_csv(file_name, engine='python', encoding=encoding)
        elif file_name.endswith('.xlsx'):
            data = pd.read_excel(file_name)
        else:
            print('unknown file format:', file_name)
    except Exception as e:
        print('error happended:', file_name)

    return data


def get_dir_file_names(dir_name):
    ret_list = []
    for root, dirs, files in os.walk(dir_name):
        for file_path in files:
            ret_list.append(os.path.join(root, file_path))

    return ret_list


def merge_file(dir_names, district='futianqu', columns=None):
    total_files = get_dir_file_names(dir_names)
    data = pd.DataFrame()

    for file_name in total_files:
        if district in file_name:
            df_data = read_data(file_name)
            df_data.columns = columns
            data = data.append(df_data, ignore_index=True)

    return data

if __name__ == '__main__':
    input_dir = r'/Users/a123/PycharmProjects/lianjia-beike-spider/data/ke/ershou'
    merge_district = r'futianqu'
    out_file = os.path.join('/Users/a123/PycharmProjects/lianjia-beike-spider/data/ke/sz', merge_district+'.csv')
    print(out_file)
    xiaoqu_columns = [r'日期', r'区', r'片区', r'小区', r'参考均价', r'在售套数', r'房屋年代', r'90天成交', r'在租房源', r'户型数',
               r'建筑类型', r'物业费用', r'物业公司', r'开发商', r'楼栋总数', r'房屋总数']

    ershou_columns = [r'日期', r'区', r'片区', r'小区', r'参考均价', r'关注人数', r'发布时间'] + HOUSE_DETAIL_INFO + \
                     ['建筑年代']

    df_data = merge_file(input_dir, merge_district, ershou_columns)
    df_data.to_csv(out_file, index=False, encoding='utf-8-sig')
