import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts

# 加载数据
file_path = 'all.csv'
data = pd.read_csv(file_path)

# 统计男女数量
gender_counts = data['性别'].value_counts()
gender_counts.index = ['男', '女']

# 创建柱状图
bar = (
    Bar()
    .add_xaxis(gender_counts.index.tolist())
    .add_yaxis("数量", gender_counts.values.tolist(), color=['blue', 'pink'])
    .set_global_opts(
        title_opts=opts.TitleOpts(title="男女数量统计"),
        xaxis_opts=opts.AxisOpts(name="性别"),
        yaxis_opts=opts.AxisOpts(name="数量"),
    )
)

# 保存图表为 HTML 文件
output_file = '男女数量统计图.html'
bar.render(output_file)
