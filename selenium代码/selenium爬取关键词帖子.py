import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

# 用来控制页面滚动
def Transfer_Clicks(browser):
    time.sleep(5)
    try:
        browser.execute_script("window.scrollBy(0,document.body.scrollHeight)", "")
    except:
        pass
    return "Transfer successfully \n"

# 判断页面是否加载出来
def isPresent(driver):
    temp = 1
    try:
        driver.find_elements(By.CSS_SELECTOR,
                             'div.line-around.layout-box.mod-pagination > a:nth-child(2) > div > select > option')
    except:
        temp = 0
    return temp

# 插入文本到txt中
def insertToTxt(content, fileName):
    with open(fileName, "a", encoding='utf-8-sig') as file:
        file.write(content + "\n")

# 插入数据
def insert_data(elems, csv_file, name, yuedu, taolun, keyword):
    with open(csv_file, 'a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        for elem in elems:
            # 用户名
            weibo_username = elem.find_element(By.CSS_SELECTOR, 'h3.m-text-cut').text
            weibo_userlevel = "普通用户"
            # 微博等级
            try:
                weibo_userlevel_color_class = elem.find_element(By.CSS_SELECTOR, "i.m-icon").get_attribute(
                    "class").replace("m-icon ", "")
                if weibo_userlevel_color_class == "m-icon-yellowv":
                    weibo_userlevel = "黄v"
                if weibo_userlevel_color_class == "m-icon-bluev":
                    weibo_userlevel = "蓝v"
                if weibo_userlevel_color_class == "m-icon-goldv-static":
                    weibo_userlevel = "金v"
                if weibo_userlevel_color_class == "m-icon-club":
                    weibo_userlevel = "微博达人"
            except:
                weibo_userlevel = "普通用户"
            # 微博内容
            weibo_content = elem.find_element(By.CSS_SELECTOR, 'div.weibo-text').text
            shares = elem.find_element(By.CSS_SELECTOR, 'i.m-font.m-font-forward + h4').text
            comments = elem.find_element(By.CSS_SELECTOR, 'i.m-font.m-font-comment + h4').text
            likes = elem.find_element(By.CSS_SELECTOR, 'i.m-icon.m-icon-like + h4').text
            # 发布时间
            weibo_time = elem.find_element(By.CSS_SELECTOR, 'span.time').text

            # 某些微博内容中还含有话题，把话题去掉
            index = weibo_content.find(keyword)
            if index != -1:
                weibo_content = weibo_content[0:index] + weibo_content[index + len(keyword):]

            insertToTxt(weibo_content, 'test2.txt')

            writer.writerow(
                [weibo_username, weibo_userlevel, weibo_content, shares, comments, likes, weibo_time, keyword, name,
                 yuedu, taolun])
            print("当前插入数据：" + weibo_username)

# 获取当前页面的数据
def get_current_weibo_data(elems, csv_file, name, yuedu, taolun, maxWeibo):
    before = 0
    after = 0
    n = 0
    while True:
        before = after
        Transfer_Clicks(driver)
        time.sleep(3)
        elems = driver.find_elements(By.CSS_SELECTOR, 'div.card.m-panel.card9')
        print("当前包含微博最大数量：%d, n当前的值为：%d, n值到5说明已无法解析出新的微博" % (len(elems), n))
        after = len(elems)
        if after > before:
            n = 0
        if after == before:
            n += 1
        if n == 5:
            print("当前关键词最大微博数为：%d" % after)
            insert_data(elems, csv_file, name, yuedu, taolun, keyword)
            break
        if len(elems) > maxWeibo:
            print("当前微博数以达到%d条" % maxWeibo)
            insert_data(elems, csv_file, name, yuedu, taolun, keyword)
            break

# 爬虫运行
def spider(driver, csv_file, keyword, maxWeibo):
    # 创建文件
    if os.path.exists(csv_file):
        print("文件已存在")
    else:
        print("文件不存在，重新创建")
        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(
                ["用户名", "微博等级", "微博内容", "转发量", "评论量", "点赞量", "发布时间", "搜索关键词", "话题名称",
                 "话题阅读数", "话题讨论数"])

    # 加载驱动，使用浏览器打开指定网址
    driver.set_window_size(452, 790)
    time.sleep(3)

    while 1:
        driver.get('https://m.weibo.cn/')
        elems = driver.find_elements(By.CSS_SELECTOR,
                                     'div.line-around.layout-box.mod-pagination > a:nth-child(2) > div > select > option')
        break

    time.sleep(2)

    # 搜索关键词
    driver.find_element(By.XPATH, "//*[@class='m-text-cut']").click()
    time.sleep(2)
    elem = driver.find_element(By.XPATH, "//*[@type='search']")
    elem.send_keys(keyword)
    elem.send_keys(Keys.ENTER)
    time.sleep(5)

    yuedu = ''
    taolun = ''
    name = keyword

    get_current_weibo_data(elems, csv_file, name, yuedu, taolun, maxWeibo)
    time.sleep(2)

if __name__ == '__main__':
    driver = webdriver.Chrome()
    csv_file = "weibo_data.csv"
    maxWeibo = 5000
    keywords = ["丝路精神"]  # 搜索关键词列表

    for keyword in keywords:
        spider(driver, csv_file, keyword, maxWeibo)
