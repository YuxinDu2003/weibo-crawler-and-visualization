import pandas as pd
from bs4 import BeautifulSoup

# 读取CSV文件
csv_file_path = "modified_一带一路ajax_全文_official.csv"
df = pd.read_csv(csv_file_path)

# 定义一个函数来解析HTML并提取文本
def extract_text_from_html(html):
    bs = BeautifulSoup(html, 'html.parser')
    return bs.get_text()

# 应用函数到 '微博内容' 列
df['微博内容'] = df['微博内容'].apply(extract_text_from_html)

# 输出修改后的DataFrame
print(df)

# 将修改后的DataFrame保存到新的CSV文件
output_csv_file_path = "bs4_modified_一带一路ajax_全文_official.csv"
df.to_csv(output_csv_file_path, index=False, encoding='utf_8_sig')
