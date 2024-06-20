import os
import re  # 正则表达式提取文本
from jsonpath import jsonpath  # 解析json数据
import requests  # 发送请求
import pandas as pd  # 存取csv文件
import datetime  # 转换时间用
import time

# 请求头
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
    "cache-control": "max-age=0",
    "^cookie": "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWblvaF6eULus48fjk-Rlij5NHD95Qceo.f1KMpe0efWs4DqcjNi--fi-z7iKysTCH8SE-41CHFxFH8SE-4BC-RSFH8SbHWeE-R1CH81F-RBCHFeCH8SEHFeE-4Sntt; SCF=Aq96ku-DG-ZgaL91f3iuBv-Dj04RMDfZ97sPGmID9A_YBYah8J-Jm5rbu_eqBTGunGmOnpYVC-b1-p79nRSTwjY.; SUB=_2A25LTZ5ADeRhGeBM4lcY9y_PyDmIHXVoIp-IrDV6PUJbktANLRPskW1NRKbJnleBjDtGxuLBkv2__PMxw0-wX40k; ALF=1718713104; WEIBOCN_FROM=1110006030; _T_WM=66270220052; MLOGIN=1; XSRF-TOKEN=ba212f; mweibo_short_token=3e44926288; M_WEIBOCN_PARAMS=luicode^%^3D10000011^%^26lfid^%^3D231583^%^26fid^%^3D1005056028786809^%^26uicode^%^3D10000011^",
    "priority": "u=0, i",
    "^sec-ch-ua": "^\\^Microsoft",
    "sec-ch-ua-mobile": "?0",
    "^sec-ch-ua-platform": "^\\^Windows^^^",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
}


"""转换GMT时间为标准格式"""
def trans_time(v_str):
    GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
    timeArray = datetime.datetime.strptime(v_str, GMT_FORMAT)
    ret_time = timeArray.strftime("%Y-%m-%d %H:%M:%S")
    return ret_time

def getLongText(v_id):
    # 构造请求URL
    url = 'https://m.weibo.cn/statuses/extend?id=' + str(v_id)
    # 发送GET请求获取长微博内容
    r = requests.get(url, headers=headers)
    # 解析返回的JSON数据
    json_data = r.json()
    # 提取长微博的内容
    long_text = json_data['data']['longTextContent']
    # 使用正则表达式清洗微博内容中的HTML标签
    dr = re.compile(r'<[^>]+>', re.S)
    long_text2 = dr.sub('', long_text)
    # 返回清洗后的长微博内容
    return long_text2



def get_weibo_list(v_keyword, v_max_page):
    for page in range(2, v_max_page + 1):
        print('===爬取第{}页微博==='.format(page))
        time.sleep(2)  # 等待2秒，避免频繁请求被封
        # 请求地址
        url = 'https://m.weibo.cn/api/container/getIndex'
        # 请求参数
        params = {
            "containerid": "100103type=1&q={}".format(v_keyword),
            "page_type": "searchall",
            "page": page
        }
        # 发送请求
        r = requests.get(url, headers=headers, params=params)
        print(r.status_code)  # 打印请求状态码
        # 解析json数据
        cards = r.json()["data"]["cards"]
        print(len(cards))  # 打印获取到的卡片数量

        # 初始化各类数据列表
        region_name_list = []
        status_city_list = []
        status_province_list = []
        status_country_list = []
        # 遍历卡片提取信息
        for card in cards:
            try:
                region_name = card['card_group'][0]['mblog']['region_name']
                region_name_list.append(region_name)
            except:
                region_name_list.append('')
            try:
                status_city = card['card_group'][0]['mblog']['status_city']
                status_city_list.append(status_city)
            except:
                status_city_list.append('')
            try:
                status_province = card['card_group'][0]['mblog']['status_province']
                status_province_list.append(status_province)
            except:
                status_province_list.append('')
            try:
                status_country = card['card_group'][0]['mblog']['status_country']
                status_country_list.append(status_country)
            except:
                status_country_list.append('')

        # 微博内容
        text_list = jsonpath(cards, '$..mblog.text')
        # 微博内容-正则表达式数据清洗
        dr = re.compile(r'<[^>]+>', re.S)
        text2_list = []

        if not text_list:  # 如果未获取到微博内容，进入下一轮循环
            continue
        if type(text_list) == list and len(text_list) > 0:
            for text in text_list:
                text2 = dr.sub('', text)  # 正则表达式提取微博内容
                text2_list.append(text2)

        # 微博创建时间
        time_list = jsonpath(cards, '$..mblog.created_at')
        time_list = [trans_time(v_str=i) for i in time_list]

        # 微博作者
        author_list = jsonpath(cards, '$..mblog.user.screen_name')
        # 微博id
        id_list = jsonpath(cards, '$..mblog.id')
        # 判断是否存在全文
        isLongText_list = jsonpath(cards, '$..mblog.isLongText')
        idx = 0
        for i in isLongText_list:
            if i == True:
                long_text = getLongText(v_id=id_list[idx])
                text2_list[idx] = long_text
            idx += 1

        # 转发数
        reposts_count_list = jsonpath(cards, '$..mblog.reposts_count')
        # 评论数
        comments_count_list = jsonpath(cards, '$..mblog.comments_count')
        # 点赞数
        attitudes_count_list = jsonpath(cards, '$..mblog.attitudes_count')
        # 关注数
        follow_count_list = jsonpath(cards, '$..mblog.user.follow_count')
        # 粉丝数
        followers_count_list = jsonpath(cards, '$..mblog.user.followers_count')
        # 性别
        gender_list = jsonpath(cards, '$..mblog.user.gender')

        # 把列表数据保存成DataFrame数据
        df = pd.DataFrame(
            {
                '页码': [page] * len(id_list),
                '微博id': id_list,
                '微博作者': author_list,
                '发布时间': time_list,
                '微博内容': text2_list,
                '转发数': reposts_count_list,
                '评论数': comments_count_list,
                '点赞数': attitudes_count_list,
                '关注数': follow_count_list,
                '粉丝数': followers_count_list,
                '性别': gender_list,
                '发布于': region_name_list,
                'ip属地_城市': status_city_list,
                'ip属地_省份': status_province_list,
                'ip属地_国家': status_country_list,
            }
        )
        # 表头
        if os.path.exists(v_weibo_file):
            header = None
        else:
            header = ['页码', '微博id', '微博作者', '发布时间', '微博内容', '转发数', '评论数', '点赞数', '关注数',
                      '粉丝数', '性别', '发布于', 'ip属地_城市', 'ip属地_省份', 'ip属地_国家']
        # 保存到csv文件
        df.to_csv(v_weibo_file, mode='a+', index=False, header=header, encoding='utf_8_sig')
        print('csv保存成功:{}'.format(v_weibo_file))



if __name__ == '__main__':
    keyword_list = [
        '丝路经济带',
        '丝路精神',
        '丝路经济带',
        '中亚经济走廊',
        '中欧班列',
        '中国外交，一带一路',
        '中巴经济走廊',
        '丝绸之路经济带'
        '新丝绸之路',
        '海上丝绸之路',
        '六廊六路多国多港',
        '国际经济合作走廊',
        '21世纪海上丝绸之路',
        '基础设施互联互通',
        '产能合作',
        '经济走廊',
        '共建共享',
        '互利共赢',
        '政策沟通',
        '资金融通',
        '民心相通',
        '贸易畅通',
        '文化交流',
        '国际合作',
        '绿色丝绸之路',
        '创新丝绸之路',
        '健康丝绸之路',
        '数字丝绸之路',
        '可持续发展'
    ]

    for i in keyword_list:
        max_search_page = 150
        # 设置爬取的关键词语
        search_keyword = i
        # 保存文件名
        v_weibo_file = '{}follow.csv'.format(search_keyword, max_search_page)
        # 如果csv文件存在，先删除之
        if os.path.exists(v_weibo_file):
            os.remove(v_weibo_file)
            print('微博清单存在，已删除: {}'.format(v_weibo_file))
        # 调用爬取微博函数
        get_weibo_list(v_keyword=search_keyword, v_max_page=max_search_page)
        # 数据清洗-去重
        df = pd.read_csv(v_weibo_file)
        # 删除重复数据
        df.drop_duplicates(subset=['微博id'], inplace=True, keep='first')
        # 再次保存csv文件
        df.to_csv(v_weibo_file, index=False, encoding='utf_8_sig')
        print('数据清洗完成')
