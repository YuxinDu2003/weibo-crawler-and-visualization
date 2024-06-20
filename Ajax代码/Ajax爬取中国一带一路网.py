import csv
import time
import random
import requests
from urllib.parse import urlencode
from lxml import etree
import re
import datetime

def trans_time(v_str):
    """转换GMT时间为标准格式"""
    GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'  # GMT时间格式
    timeArray = datetime.datetime.strptime(v_str, GMT_FORMAT)  # 将字符串转换为时间数组
    ret_time = timeArray.strftime("%Y-%m-%d %H:%M:%S")  # 将时间数组格式化为标准时间格式
    return ret_time

def get_page(since_id):
    """获取指定since_id的微博数据"""
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
        "cache-control": "max-age=0",
        "priority": "u=0, i",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
    }

    params = {
        't': '0',
        'luicode': '10000011',
        'lfid': '231583',
        'containerid': '1076036028786809',
    }

    base_url = "https://m.weibo.cn/api/container/getIndex?"

    if since_id != 0:
        params['since_id'] = since_id  # 如果有since_id则添加到参数中

    url = base_url + urlencode(params)  # 构建完整的URL

    try:
        response = requests.get(url, headers=headers)  # 发送GET请求
        if response.status_code == 200:
            data = response.json()  # 获取JSON响应数据
            if 'cardlistInfo' in data['data']:
                return data, data['data']['cardlistInfo']['since_id']  # 返回数据和since_id
            else:
                print("No more data available or different data structure returned.")
                return None, None

    except requests.ConnectionError as e:
        print('Connection Error:', e.args)
        return None, None

def get_first_since_id(first_url):
    """获取第一页的since_id"""
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
        "cache-control": "max-age=0",
        "priority": "u=0, i",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
    }

    response = requests.get(first_url, headers=headers)  # 发送GET请求
    data = response.json()  # 获取JSON响应数据
    if 'cardlistInfo' in data['data']:
        return data['data']['cardlistInfo']['since_id']  # 返回since_id
    else:
        print("No cardlistInfo found in the first page data.")
        return None

def parse_page(data_json):
    """解析页面的微博数据"""
    if data_json and data_json.get('data') and data_json.get('cards'):
        items = data_json.get('data').get('cards')  # 获取微博列表
        if items is not None:
            for item in items:
                if item and 'mblog' in item:
                    weibo = {}
                    weibo['点赞数'] = item['mblog'].get('attitudes_count')
                    weibo['评论数'] = item['mblog'].get('comments_count')
                    weibo['转发数'] = item['mblog'].get('reposts_count')
                    weibo['发布时间'] = trans_time(item['mblog'].get('created_at'))

                    if item['mblog'].get('isLongText') == True:
                        id = item['mblog'].get('id')
                        url = 'https://m.weibo.cn/detail/' + str(id)  # 构建长微博详情URL
                        long_text_headers = {
                            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
                            "cache-control": "max-age=0",
                            "priority": "u=0, i",
                            "sec-fetch-dest": "empty",
                            "sec-fetch-mode": "navigate",
                            "sec-fetch-site": "same-origin",
                            "upgrade-insecure-requests": "1",
                            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
                        }
                        response = requests.get(url, headers=long_text_headers)  # 发送GET请求获取长微博内容
                        if response.status_code == 200:
                            text_elements = re.findall(r'"text": ".*（.*）', response.text)  # 正则提取微博文本
                            weibo['微博内容'] = ''.join(text_elements) if text_elements else "未找到文本"
                    else:
                        html = item['mblog'].get('text')
                        tree = etree.HTML(html)  # 将HTML转换为lxml树
                        weibo['微博内容'] = ''.join(tree.xpath('//text()'))  # 提取文本内容

                    yield weibo
                else:
                    continue

def save_to_csv(data, csv_writer):
    """保存数据到CSV文件"""
    for result in data:
        csv_writer.writerow(result)

def main():
    with open("一带一路ajax_全文_official.csv", 'w', newline='', encoding='utf-8-sig') as f:
        name = ['点赞数', '评论数', '转发数', '发布时间', '微博内容']
        csv_writer = csv.DictWriter(f, fieldnames=name)
        csv_writer.writeheader()

        first_url = 'https://m.weibo.cn/api/container/getIndex?t=0&luicode=10000011&lfid=231583&containerid=1076036028786809'
        data_json, since_id = get_page(0)  # 获取第一页数据
        if data_json:
            results = list(parse_page(data_json))  # 解析数据
            save_to_csv(results, csv_writer)  # 保存到CSV

            first_since_id = get_first_since_id(first_url)  # 获取第一页的since_id
            if first_since_id:
                data_json, since_id = get_page(first_since_id)  # 获取第二页数据
                if data_json:
                    results = list(parse_page(data_json))  # 解析数据
                    save_to_csv(results, csv_writer)  # 保存到CSV

                    max_page = 1000  # 最大页数
                    for i in range(max_page - 2):
                        data_json, since_id = get_page(since_id)  # 获取下一页数据
                        if not data_json:
                            print("No more data available.")
                            break
                        results = list(parse_page(data_json))  # 解析数据
                        delay_seconds = random.uniform(1, 5)  # 设置随机延迟时间
                        time.sleep(delay_seconds)  # 以秒为单位的延迟
                        save_to_csv(results, csv_writer)  # 保存到CSV
                else:
                    print("Failed to get data after first page.")
            else:
                print("Failed to get first since_id.")
        else:
            print("Failed to get initial data.")

if __name__ == "__main__":
    main()
