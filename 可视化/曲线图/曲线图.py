import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.font_manager import FontProperties

# 加载数据
file_path = '一带一路相关民间微博发文前2000页follow.csv'  # 替换为你的实际文件路径
data = pd.read_csv(file_path)

# 处理时间格式
def date_deal(string):
    if isinstance(string, str):
        return datetime.strptime(string, '%Y-%m-%d %H:%M').strftime('%Y-%m-%d')
    else:
        return None

# 确保日期列是字符串类型，并处理NaN值
data['发布时间'] = data['发布时间'].astype(str).apply(date_deal)

# 删除包含无效日期的行
data = data.dropna(subset=['发布时间'])

# 统计每一天的点赞数、评论数、转发数
data['发布时间'] = pd.to_datetime(data['发布时间'])
daily_data = data.groupby(data['发布时间'].dt.date).agg({
    '点赞数': 'sum',
    '评论数': 'sum',
    '转发数': 'sum'
}).reset_index()

# 设置中文字体
font = FontProperties(fname=r'C:\Windows\Fonts\FZSTK.TTF')  # 替换为你的字体路径

# 绘制图表
plt.figure(figsize=(12, 6))

plt.plot(daily_data['发布时间'], daily_data['点赞数'], label='点赞数')
plt.plot(daily_data['发布时间'], daily_data['评论数'], label='评论数')
plt.plot(daily_data['发布时间'], daily_data['转发数'], label='转发数')

plt.xlabel('日期', fontproperties=font)
plt.ylabel('数量', fontproperties=font)
plt.title('点赞数、评论数、转发数随时间变化图', fontproperties=font)
plt.legend(prop=font)
plt.grid(True)
plt.xticks(rotation=45, fontproperties=font)
plt.tight_layout()

# 保存图表
output_file = '点赞数_评论数_转发数_随时间变化图.png'  # 替换为你希望保存的路径
plt.savefig(output_file)
plt.show()
