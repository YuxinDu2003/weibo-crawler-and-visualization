import pandas as pd

# 加载数据时指定编码方式
file_path = 'all.csv'
data = pd.read_csv(file_path, encoding='utf-8-sig')

# 筛选出 'ip属地_国家' 列值为 '中国' 且 'ip属地_省份' 列无缺失值的行
cleaned_data = data[(data['ip属地_国家'] == '中国') & (data['ip属地_省份'].notna())]

# 将清洗后的数据保存到一个新的CSV文件
cleaned_file_path = 'cleaned_all.csv'
cleaned_data.to_csv(cleaned_file_path, index=False, encoding='utf-8-sig')
