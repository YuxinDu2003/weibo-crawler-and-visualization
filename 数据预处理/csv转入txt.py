import pandas as pd
import os
import glob

# 指定CSV文件所在的文件夹路径
folder_path = r'D:\python_project\数据采集与可视化课程\大作业\data'

# 获取文件夹中的所有CSV文件
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

# 对每个CSV文件进行处理
for csv_file in csv_files:
    # 读取CSV文件
    data = pd.read_csv(csv_file)

    # 指定要提取的列名
    columns_to_extract = ['微博内容']

    # 提取指定列的数据
    extracted_data = data[columns_to_extract]

    # 获取输入文件名（不包含扩展名）
    base_filename = os.path.splitext(os.path.basename(csv_file))[0]

    # 生成输出TXT文件名
    txt_file = f'{base_filename}.txt'

    # 将提取的列保存到TXT文件，指定编码为utf-8-sig
    with open(txt_file, 'w', encoding='utf-8-sig') as f:
        # 写入列名作为第一行
        f.write('\t'.join(columns_to_extract) + '\n')
        # 写入数据行
        for index, row in extracted_data.iterrows():
            f.write('\t'.join(map(str, row.values)) + '\n')

    print(f"数据已成功保存到 {txt_file}")
