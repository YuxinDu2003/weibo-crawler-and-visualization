import pandas as pd
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import ChartType

# 加载清洗后的数据
file_path = 'cleaned_all.csv'
data = pd.read_csv(file_path)

# 省份名称映射（确保与pyecharts一致）
province_map = {
    "北京": "北京市",
    "天津": "天津市",
    "上海": "上海市",
    "重庆": "重庆市",
    "河北": "河北省",
    "山西": "山西省",
    "辽宁": "辽宁省",
    "吉林": "吉林省",
    "黑龙江": "黑龙江省",
    "江苏": "江苏省",
    "浙江": "浙江省",
    "安徽": "安徽省",
    "福建": "福建省",
    "江西": "江西省",
    "山东": "山东省",
    "河南": "河南省",
    "湖北": "湖北省",
    "湖南": "湖南省",
    "广东": "广东省",
    "海南": "海南省",
    "四川": "四川省",
    "贵州": "贵州省",
    "云南": "云南省",
    "陕西": "陕西省",
    "甘肃": "甘肃省",
    "青海": "青海省",
    "台湾": "台湾省",
    "内蒙古": "内蒙古自治区",
    "广西": "广西壮族自治区",
    "西藏": "西藏自治区",
    "宁夏": "宁夏回族自治区",
    "新疆": "新疆维吾尔自治区",
    "香港": "香港特别行政区",
    "澳门": "澳门特别行政区"
}

# 映射省份名称
data['ip属地_省份'] = data['ip属地_省份'].map(province_map)

# 统计各省份出现的频率
province_counts = data['ip属地_省份'].value_counts().reset_index()
province_counts.columns = ['省份', '频率']

# 检查地名是否存在于 pyecharts 的地理坐标数据库中
geo = Geo()
valid_province_data = []
for province, count in zip(province_counts['省份'], province_counts['频率']):
    if geo.get_coordinate(province):
        valid_province_data.append([province, count])

# 创建地理热力图
geo = (
    Geo()
    .add_schema(maptype="china")
    .add(
        "频率",
        valid_province_data,
        type_=ChartType.HEATMAP,
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            min_=0, max_=1000,
            range_color=["#87CEEB", "#FFA500", "#FF4500", "#FF0000"]
        ),
        title_opts=opts.TitleOpts(title="中国地理分布密度图"),
    )
)

# 保存图表为 HTML 文件
output_file = '中国地理分布密度图.html'
geo.render(output_file)
