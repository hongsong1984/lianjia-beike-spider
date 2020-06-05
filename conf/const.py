__author__ = 'a123'

# 爬虫网站配置
LIANJIA_SPIDER = "lianjia"
BEIKE_SPIDER = "ke"
# SPIDER_NAME = LIANJIA_SPIDER

# 房屋详细信息字段keys
HOUSE_DETAIL_INFO = ['房屋户型', '所在楼层', '建筑面积', '套内面积', '房屋朝向', '户型结构', '梯户比例', '建筑类型', '建筑结构',
                     '装修情况', '挂牌时间', '交易权属', '上次交易', '房屋用途', '房屋年限', '配备电梯', '产权所属', '抵押信息',
                     '房本备件', '房协编码']


# 房屋成交信息字段keys
DEAL_DETAIL_INFO = ['挂牌价格（万）', '成交周期（天）', '调价（次）', '带看（次）', '关注（人）', '浏览（次）', '房屋户型', '所在楼层',
                    '建筑面积', '套内面积', '房屋朝向', '户型结构', '梯户比例', '建筑类型', '建筑结构', '建成年代', '装修情况',
                    '挂牌时间', '交易权属', '房屋用途', '房屋年限', '配备电梯', '房权所属', '链家编号', '历史成交']


SZ_AREAS = ['baishida', 'buxin', 'chunfenglu', 'cuizhu', 'diwang', 'dongmen', 'honghu', 'huangbeiling', 'huangmugang', 'liantang', 'luohukouan', 'luoling', 'qingshuihe', 'sungang', 'wanxiangcheng', 'xinxiu', 'yinhu', 'bagualing', 'baihua', 'chegongmiao', 'chiwei', 'futianbaoshuiqu', 'futianzhongxin', 'huanggang', 'huangmugang', 'huaqiangbei', 'huaqiangnan', 'jingtian', 'lianhua', 'meilin', 'shangbu', 'shangxiasha', 'shawei', 'shixia', 'xiangmeibei', 'xiangmihu', 'xinzhou1', 'yinhu', 'yuanling', 'zhuzilin', 'baishizhou', 'daxuecheng3', 'hongshuwan', 'houhai', 'huaqiaocheng1', 'kejiyuan', 'nanshanzhongxin', 'nantou', 'qianhai', 'shekou', 'shenzhenwan', 'xili1', 'meisha', 'shatoujiao', 'yantiangang', 'baoanzhongxin', 'bihai1', 'fanshen', 'fuyong', 'shajing', 'shiyan', 'songgang', 'taoyuanju', 'xicheng1', 'xinan', 'xixiang', 'bantian', 'bujidafen', 'bujiguan', 'bujijie', 'bujinanling', 'bujishiyaling', 'bujishuijing', 'danzhutou', 'dayunxincheng', 'henggang', 'longgangbaohe', 'longgangshuanglong', 'longgangzhongxincheng', 'minzhi', 'pingdi', 'pinghu', 'guanlan', 'hongshan6', 'longhuaxinqu', 'longhuazhongxin', 'meilinguan', 'minzhi', 'shangtang', 'shiyan', 'gongming', 'pingshan', 'dapengbandao']

SZ_DISTRICT_AREAS = {'baishida': 'luohuqu', 'buxin': 'luohuqu', 'chunfenglu': 'luohuqu',
                     'cuizhu': 'luohuqu', 'diwang': 'luohuqu', 'dongmen': 'luohuqu',
                     'honghu': 'luohuqu', 'huangbeiling': 'luohuqu', 'huangmugang': 'futianqu',
                     'liantang': 'luohuqu', 'luohukouan': 'luohuqu', 'luoling': 'luohuqu',
                     'qingshuihe': 'luohuqu', 'sungang': 'luohuqu', 'wanxiangcheng': 'luohuqu',
                     'xinxiu': 'luohuqu', 'yinhu': 'futianqu', 'bagualing': 'futianqu',
                     'baihua': 'futianqu', 'chegongmiao': 'futianqu', 'chiwei': 'futianqu',
                     'futianbaoshuiqu': 'futianqu', 'futianzhongxin': 'futianqu',
                     'huanggang': 'futianqu', 'huaqiangbei': 'futianqu', 'huaqiangnan': 'futianqu',
                     'jingtian': 'futianqu', 'lianhua': 'futianqu', 'meilin': 'futianqu',
                     'shangbu': 'futianqu', 'shangxiasha': 'futianqu', 'shawei': 'futianqu',
                     'shixia': 'futianqu', 'xiangmeibei': 'futianqu', 'xiangmihu': 'futianqu',
                     'xinzhou1': 'futianqu', 'yuanling': 'futianqu', 'zhuzilin': 'futianqu',
                     'baishizhou': 'nanshanqu', 'daxuecheng3': 'nanshanqu', 'hongshuwan': 'nanshanqu',
                     'houhai': 'nanshanqu', 'huaqiaocheng1': 'nanshanqu', 'kejiyuan': 'nanshanqu',
                     'nanshanzhongxin': 'nanshanqu', 'nantou': 'nanshanqu', 'qianhai': 'nanshanqu',
                     'shekou': 'nanshanqu', 'shenzhenwan': 'nanshanqu', 'xili1': 'nanshanqu',
                     'meisha': 'yantianqu', 'shatoujiao': 'yantianqu', 'yantiangang': 'yantianqu',
                     'baoanzhongxin': 'baoanqu', 'bihai1': 'baoanqu', 'fanshen': 'baoanqu',
                     'fuyong': 'baoanqu', 'shajing': 'baoanqu', 'shiyan': 'longhuaqu',
                     'songgang': 'baoanqu', 'taoyuanju': 'baoanqu', 'xicheng1': 'baoanqu',
                     'xinan': 'baoanqu', 'xixiang': 'baoanqu', 'bantian': 'longgangqu',
                     'bujidafen': 'longgangqu', 'bujiguan': 'longgangqu', 'bujijie': 'longgangqu',
                     'bujinanling': 'longgangqu', 'bujishiyaling': 'longgangqu',
                     'bujishuijing': 'longgangqu', 'danzhutou': 'longgangqu', 'dayunxincheng': 'longgangqu',
                     'henggang': 'longgangqu', 'longgangbaohe': 'longgangqu', 'longgangshuanglong': 'longgangqu',
                     'longgangzhongxincheng': 'longgangqu', 'minzhi': 'longhuaqu', 'pingdi': 'longgangqu',
                     'pinghu': 'longgangqu', 'guanlan': 'longhuaqu', 'hongshan6': 'longhuaqu',
                     'longhuaxinqu': 'longhuaqu', 'longhuazhongxin': 'longhuaqu', 'meilinguan': 'longhuaqu',
                     'shangtang': 'longhuaqu', 'gongming': 'guangmingqu', 'pingshan': 'pingshanqu',
                     'dapengbandao': 'dapengxinqu'}

# 福田区
# SZ_FUTIAN_AREAS = ['bagualing', 'baihua', 'chegongmiao', 'chiwei', 'futianbaoshuiqu', 'futianzhongxin',
#                    'huanggang', 'huangmugang', 'huaqiangbei', 'huaqiangnan', 'jingtian', 'lianhua',
#                    'meilin', 'shangbu', 'shangxiasha', 'shawei', 'shixia', 'xiangmeibei', 'xiangmihu',
#                    'xinzhou1', 'yinhu', 'yuanling', 'zhuzilin']
SZ_FUTIAN_AREAS = ['huanggang', 'huaqiangbei', 'huaqiangnan', 'jingtian', 'lianhua',
                   'meilin', 'shangbu', 'shangxiasha', 'shawei', 'shixia', 'xiangmeibei', 'xiangmihu',
                   'xinzhou1', 'yinhu', 'yuanling', 'zhuzilin']

SZ_FUTIAN_DISTRICT_AREAS = {area: r'futianqu' for area in SZ_FUTIAN_AREAS}

SZ_CHINESE_AREAS = {'bagualing': '八卦岭', 'baihua': '百花', 'chegongmiao': '车公庙',
                    'chiwei': '赤尾', 'futianbaoshuiqu': '福田保税区', 'futianzhongxin': r'福田中心',
                    'huanggang': '皇岗', 'huangmugang': '黄木岗', 'huaqiangbei': '华强北',
                    'huaqiangnan': '华强南', 'jingtian': '景田', 'lianhua': '莲花',
                    'meilin': '梅林', 'shangbu': '上步', 'shangxiasha': '上下沙', 'shawei': '沙尾',
                    'shixia': '石厦', 'xiangmeibei': '香梅北', 'xiangmihu': '香蜜湖',
                    'xinzhou1': r'新洲', 'yinhu': '银湖', 'yuanling': '园岭', 'zhuzilin': '竹子林',
                    'baishizhou': '白石洲', 'daxuecheng3': '大学城', 'hongshuwan': '红树湾',
                    'houhai': '后海', 'huaqiaocheng1': '华侨城', 'kejiyuan': r'科苑',
                    'nanshanzhongxin': '南山中心', 'nantou': '南头', 'qianhai': '前海',
                    'shekou': '蛇口', 'shenzhenwan': '深圳湾', 'xili1': '西丽'}


# 南山区
# SZ_NANSHAN_AREAS = ['baishizhou', 'daxuecheng3', 'hongshuwan', 'houhai', 'huaqiaocheng1',
#                     'kejiyuan', 'nanshanzhongxin', 'nantou', 'qianhai', 'shekou', 'shenzhenwan', 'xili1']

SZ_NANSHAN_AREAS = ['nanshanzhongxin', 'shekou', 'shenzhenwan', 'xili1']

SZ_NANSHAN_DISTRICT_AREAS = {area: r'nanshanqu' for area in SZ_NANSHAN_AREAS}

