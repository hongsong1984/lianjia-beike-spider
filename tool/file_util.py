#!/usr/bin/env python
# coding=utf-8

import os
import pandas as pd
from conf.const import HOUSE_DETAIL_INFO
from lib.utility.date import get_date_string


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
    merge_type = r'ershou'        # r'ershou'
    merge_district = r'nanshanqu' # r'nanshanqu'

    today = get_date_string()
    input_dir = r'/Users/a123/PycharmProjects/lianjia-beike-spider/data/ke/'+ merge_type + r'/sz/'+today
    print('input_dir:', input_dir)
    out_file = os.path.join('/Users/a123/PycharmProjects/lianjia-beike-spider/data/ke/sz',
                            merge_district+r'_'+ merge_type +'.csv')
    print('out_file:', out_file)


    xiaoqu_columns = [r'日期', r'区', r'片区', r'小区', r'参考均价', r'在售套数', r'房屋年代', r'90天成交', r'在租房源', r'户型数',
               r'建筑类型', r'物业费用', r'物业公司', r'开发商', r'楼栋总数', r'房屋总数']

    ershou_columns = [r'日期', r'区', r'片区', r'小区', r'总价', r'关注人数', r'发布时间'] + HOUSE_DETAIL_INFO + \
                     ['建筑年代']

    columns = []
    if merge_type == r'xiaoqu':
        columns = xiaoqu_columns
    elif merge_type == r'ershou':
        columns = ershou_columns
    else:
        print('error merge_type', merge_type)

    df_data = merge_file(input_dir, merge_district, columns)
    if merge_type == r'ershou':
        df_data['总价'] = df_data['总价'].map(lambda x: x.rstrip('万'))
        df_data['建筑面积'] = df_data['建筑面积'].map(lambda x: x.rstrip('㎡'))
        df_data['参考均价'] =df_data.apply(lambda x: '%.2f' % (10000* float(x['总价']) / float(x['建筑面积']) ), axis=1)
        df_data.insert(5, '参考均价', df_data.pop('参考均价'))


    df_data.to_csv(out_file, index=False, encoding='utf-8-sig')
