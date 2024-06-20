from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
import jieba.posseg as pseg
from collections import Counter
import PIL.Image as Image
from matplotlib import colors

# 读取文本文件
text = open("一带一路.txt", encoding="utf-8-sig").read()
words = pseg.cut(text)

# 提取指定长度和词性的词语
report_words = []
for word, flag in words:
    if (len(word) >= 2) and ('n' in flag):  # 这里只统计名词
        report_words.append(word)

# 统计高频词汇
result = Counter(report_words).most_common(200)  # 词的个数

# 建立词汇字典
content = dict(result)

# 输出词频统计结果
for i in range(min(50, len(result))):  # 避免 result 长度小于 50 的情况
    word, freq = result[i]
    print("{0:<10}{1:>5}".format(word, freq))

# 设置停用词
stopwords = set(STOPWORDS)
stopwords.update(["的", "新华社", "以上", "报告", "表示诚挚感谢", "全文"])

# 读取掩膜图像
background = Image.open("11.png").convert('RGB')
mask = np.array(background)

# 设置字体样式路径
font_path = r'C:\Windows\Fonts\FZSTK.TTF'

# 设置字体大小
max_font_size = 100
min_font_size = 5

# 建立颜色数组
color_list = ['#FF274B', '#FF5733', '#FF8D1A', '#FFC300', '#DAF7A6', '#33FF57', '#33FFBD', '#33CFFF', '#335BFF', '#8D33FF']
# 调用颜色数组
colormap = colors.ListedColormap(color_list)

# 自定义颜色函数
def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return colormap.colors[np.random.randint(0, len(color_list))]

# 生成词云
wordcloud = WordCloud(scale=4,  # 输出清晰度
                      font_path=font_path,  # 字体路径
                      width=1600,  # 输出图片宽度
                      height=900,  # 输出图片高度
                      background_color='white',  # 图片背景颜色
                      stopwords=stopwords,  # 停用词
                      mask=mask,  # 掩膜
                      max_font_size=max_font_size,  # 最大字体大小
                      min_font_size=min_font_size,  # 最小字体大小
                      max_words=200,  # 词云图中显示的最大词汇数量
                      color_func=color_func  # 每个词的颜色不同
                      ).generate_from_frequencies(content)

# 使用 matplotlib 显示词云
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# 保存词云图
wordcloud.to_file("wordcloud.png")
