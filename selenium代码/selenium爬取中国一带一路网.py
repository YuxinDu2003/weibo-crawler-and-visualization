import time
import pandas as pd
from selenium import webdriver  # 导入Selenium WebDriver库
from selenium.webdriver.common.by import By  # 导入Selenium的By模块，用于定位元素
from selenium.webdriver.common.keys import Keys  # 导入Selenium的Keys模块，用于发送键盘输入
from selenium.webdriver.support.ui import WebDriverWait  # 导入Selenium的WebDriverWait模块，用于显式等待
from selenium.webdriver.support import expected_conditions as EC  # 导入Selenium的expected_conditions模块，用于条件判断
import re  # 导入正则表达式模块

def initialize_driver():
    """初始化并返回Selenium的WebDriver"""
    driver = webdriver.Chrome()  # 启动Chrome浏览器
    driver.get('https://m.weibo.cn')  # 打开微博网页
    time.sleep(3)  # 等待页面加载
    return driver

def search_topic(driver, topic):
    """在微博上搜索指定话题"""
    search_button = driver.find_element(By.XPATH,
                                        "//a[@class='nav-search unlogin-search']/aside/label[@class='m-search']/div[@class='m-text-cut']")
    search_button.click()  # 点击搜索按钮
    time.sleep(2)  # 等待搜索页面加载

    search_input = driver.find_element(By.XPATH, "//input[@type='search']")
    search_input.send_keys(topic)  # 输入搜索关键词
    time.sleep(2)  # 等待输入完成
    search_input.send_keys(Keys.RETURN)  # 按回车键开始搜索
    time.sleep(2)  # 等待搜索结果加载

def click_first_result(driver):
    """点击搜索结果中的第一个链接"""
    try:
        web_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "/html/body/div[@id='app']/div[1]/div[1]/div[@class='card card11'][1]/div/div[@class='card-list']/div[@class='card m-panel card28 m-avatar-box']/div[@class='card-wrap']/div[@class='card-main']/div[@class='m-box']/div[@class='m-box-col m-box-dir m-box-center']/div[@class='m-text-box']/h3[@class='m-text-cut']/span"))
        )
        web_button.click()  # 点击第一个搜索结果
    except Exception as e:
        print(f"Error: {e}")

def scroll_to_load_more(driver, scroll_times=3):
    """向下滚动页面以加载更多内容"""
    previous_height = driver.execute_script("return document.body.scrollHeight")  # 获取当前页面高度
    count = 0
    while count < scroll_times:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 滚动到页面底部
            time.sleep(3)  # 等待新内容加载
            new_height = driver.execute_script("return document.body.scrollHeight")  # 获取新页面高度
            if new_height == previous_height:  # 判断是否到底
                print("Reached the end of the page.")
                break
            previous_height = new_height  # 更新页面高度
            count += 1
        except Exception as e:
            print(f"Scrolling Error: {e}")
            break

def extract_texts(driver):
    """提取微博文章的文本内容"""
    text = []
    try:
        articles = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='card m-panel card9 weibo-member']/div[@class='card-wrap']/div[@class='card-main']/article[@class='weibo-main']/div[@class='weibo-og']//div[@class='weibo-text']"))
        )
        for article in articles:
            try:
                expand_link = article.find_element(By.XPATH, ".//a[@class='WB_text_opt']")
                if expand_link.is_displayed() and expand_link.text.startswith('展开全文'):  # 如果存在“展开全文”链接
                    expand_link.click()  # 点击展开全文
                    time.sleep(1)  # 等待全文加载
                    full_content = article.find_element(By.XPATH, ".//p[@node-type='feed_list_content_full']").text
                    text.append(full_content)  # 获取全文内容
                else:
                    text.append(article.text)  # 获取短文本内容
            except Exception as e:
                text.append(article.text)  # 如果展开失败，获取短文本内容
    except Exception as e:
        print(f"Error: {e}")
    return text

def extract_numbers(driver, xpath):
    """根据指定的XPath提取数值信息"""
    numbers = []
    try:
        elements = driver.find_elements(By.XPATH, xpath)  # 根据XPath定位元素
        for element in elements:
            number_pattern = re.compile(r"\d+")  # 定义数字模式
            numbers_found = number_pattern.findall(element.text)  # 提取文本中的数字
            if not numbers_found:
                numbers_found.append(0)  # 如果未找到数值则设为0
            numbers_as_int = list(map(int, numbers_found))  # 将字符串转换为整数
            numbers.append(numbers_as_int[0])
    except Exception as e:
        print(f"Error extracting numbers: {e}")
    return numbers

def save_to_csv(data, filename):
    """将数据保存到CSV文件中"""
    try:
        df = pd.DataFrame(data)  # 将数据转换为DataFrame
        df.to_csv(filename, encoding='utf-8-sig', index=False)  # 保存为CSV文件
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def main():
    """主函数，运行整个爬虫程序"""
    driver = initialize_driver()  # 初始化WebDriver
    search_topic(driver, '一带一路')  # 搜索关键词
    click_first_result(driver)  # 点击第一个搜索结果
    scroll_to_load_more(driver, scroll_times=3)  # 滚动三次以加载更多内容

    text = extract_texts(driver)  # 提取文本内容
    reposts = extract_numbers(driver, "//footer[@class='m-ctrl-box m-box-center-a']/div[1]/h4")  # 提取转发数
    comments = extract_numbers(driver, "//footer[@class='m-ctrl-box m-box-center-a']/div[2]/h4")  # 提取评论数
    attitudes = extract_numbers(driver, "//footer[@class='m-ctrl-box m-box-center-a']/div[3]/h4")  # 提取点赞数

    min_length = min(len(text), len(reposts), len(comments), len(attitudes))  # 确保数据长度一致

    data = {
        'attitudes': attitudes[:min_length],
        'comments': comments[:min_length],
        'reposts': reposts[:min_length],
        'text': text[:min_length]
    }

    save_to_csv(data, '一带一路selenium_全文.csv')  # 保存数据到CSV文件

    time.sleep(2)
    driver.quit()  # 关闭浏览器

if __name__ == "__main__":
    main()
