import os
import glob
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# 定义读取TXT文件内容的函数
def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        return f.read()

# 读取停用词
def load_stopwords(stopwords_file):
    with open(stopwords_file, 'r', encoding='utf-8') as f:
        stopwords = set(f.read().split())
    return stopwords

# 分词并去除停用词
def process_text(text, stopwords):
    words = jieba.cut(text)
    filtered_words = [word for word in words if word not in stopwords and len(word) > 1]
    return ' '.join(filtered_words)

# 读取停用词文件
stopwords_file = 'stopwords.txt'
stopwords = load_stopwords(stopwords_file)

# 文件夹路径
folder_path = r'D:\python_project\数据采集与可视化课程\大作业\data'
# 获取文件夹中的所有TXT文件
txt_files = glob.glob(os.path.join(folder_path, '*.txt'))

# 加载背景图片
background_image_path = '中国地图.png'
background_image = np.array(Image.open(background_image_path))

# 定义颜色函数
def random_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl({}, {}%, {}%)".format(np.random.randint(0, 360), np.random.randint(50, 100), np.random.randint(25, 75))

# 对每个TXT文件生成词云图
for txt_file in txt_files:
    # 读取TXT文件内容
    text = read_txt_file(txt_file)
    # 处理文本
    processed_text = process_text(text, stopwords)

    # 生成词云
    wordcloud = WordCloud(
        width=800, height=800,
        background_color='white',
        mask=background_image,
        font_path= r'C:\Program Files\Microsoft Office\root\vfs\Fonts\private\simkai.ttf',  # 替换为你需要的正式字体路径
        contour_color='black',
        contour_width=1,
        color_func=random_color_func  # 设置颜色函数
    ).generate(processed_text)

    # 显示词云图
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    # 保存词云图
    base_filename = os.path.splitext(os.path.basename(txt_file))[0]
    output_image_path = os.path.join(folder_path, f'{base_filename}_wordcloud.png')
    wordcloud.to_file(output_image_path)
    print(f"词云图已保存为 {output_image_path}")
