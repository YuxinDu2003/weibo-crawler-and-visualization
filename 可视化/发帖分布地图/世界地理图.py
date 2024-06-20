import pandas as pd
from pyecharts.charts import Map
from pyecharts import options as opts

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

# 将国家和频率转换为 pyecharts 需要的格式
country_data = [list(z) for z in zip(country_counts['国家'], country_counts['频率'])]

# 创建世界地图
map_chart = (
    Map()
    .add("频率", country_data, "world")
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 不显示国家名称
    .set_global_opts(
        title_opts=opts.TitleOpts(title="世界地理图"),
        visualmap_opts=opts.VisualMapOpts(
            is_piecewise=True,
            pieces=[
                {"min": 100, "label": "100+", "color": "#8B0000"},
                {"min": 80, "max": 100, "label": "80 - 100", "color": "#FF0000"},
                {"min": 60, "max": 80, "label": "60 - 80", "color": "#FF4500"},
                {"min": 40, "max": 60, "label": "40 - 60", "color": "#FFA500"},
                {"min": 20, "max": 40, "label": "20 - 40", "color": "#ADFF2F"},
                {"min": 0, "max": 20, "label": "0 - 20", "color": "#87CEEB"},
            ],
        ),
    )
)

# 保存图表为 HTML 文件
output_file = '世界地理图.html'
map_chart.render(output_file)
