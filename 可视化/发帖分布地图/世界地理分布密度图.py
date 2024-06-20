import pandas as pd
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import ChartType

# 加载数据
file_path = 'all.csv'
data = pd.read_csv(file_path)

# 国家名称映射
country_map = {
    "中国": "China",
    "美国": "United States",
    "加拿大": "Canada",
    "法国": "France",
    "德国": "Germany",
    "英国": "United Kingdom",
    "澳大利亚": "Australia",
    "俄罗斯": "Russia",
    "日本": "Japan",
    "韩国": "South Korea",
    "印度": "India",
    "哈萨克斯坦": "Kazakhstan",
    "马来西亚": "Malaysia",
    "新加坡": "Singapore",
    "印度尼西亚": "Indonesia",
    "希腊": "Greece",
    "巴基斯坦": "Pakistan",
    "白俄罗斯": "Belarus",
    "坦桑尼亚": "Tanzania",
    "新西兰": "New Zealand",
    "多哥": "Togo",
    "摩洛哥": "Morocco",
    "菲律宾": "Philippines",
    "安哥拉": "Angola",
    "泰国": "Thailand",
    "意大利": "Italy",
    "阿根廷": "Argentina",
    "越南": "Vietnam",
    "瑞士": "Switzerland",
    "伊朗": "Iran",
    "柬埔寨": "Cambodia",
    "巴西": "Brazil",
    "塞尔维亚": "Serbia",
    "阿联酋": "United Arab Emirates",
    "沙特阿拉伯": "Saudi Arabia",
    "斯里兰卡": "Sri Lanka",
}

# 映射国家名称
data['ip属地_国家'] = data['ip属地_国家'].map(country_map).fillna(data['ip属地_国家'])

# 统计各国家出现的频率
country_counts = data['ip属地_国家'].value_counts().reset_index()
country_counts.columns = ['国家', '频率']

# 检查地名是否存在于 pyecharts 的地理坐标数据库中
geo = Geo()
valid_country_data = []
for country, count in zip(country_counts['国家'], country_counts['频率']):
    coord = geo.get_coordinate(country)
    if coord:
        valid_country_data.append([country, count])
    else:
        print(f"'{country}' 坐标不存在")

# 创建地理热力图
geo = (
    Geo()
    .add_schema(maptype="world")
    .add(
        "频率",
        valid_country_data,
        type_=ChartType.HEATMAP,
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            min_=0, max_=1000,
            range_color=["#87CEEB", "#FFA500", "#FF4500", "#FF0000"]
        ),
        title_opts=opts.TitleOpts(title="世界地理分布密度图"),
    )
)

# 保存图表为 HTML 文件
output_file = '世界地理分布密度图.html'
geo.render(output_file)
