import pandas as pd

# 假设CSV文件路径为 'your_csv_file.csv'
csv_file_path = "一带一路ajax_全文_folk.csv"

# 读取CSV文件
df = pd.read_csv(csv_file_path)

# 删除句子前面的"text"以及相关标点
df['微博内容'] = df['微博内容'].str.replace(r'"text": "', '', regex=True)
# 对于未找到文本的行进行删除
df = df[df['微博内容'] != '未找到文本']
# 删除空行
df = df.dropna(subset=['微博内容'])

# 保存修改后的CSV文件
output_csv_file_path = "modified_一带一路ajax_全文_folk.csv"
df.to_csv(output_csv_file_path, index=False, encoding='utf_8_sig')


