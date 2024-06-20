import pandas as pd
import os

# 定义文件夹路径和保存路径
folder_path = r"D:\python_project\数据采集与可视化课程\大作业\ajax\folk"
save_file_path = r"D:\python_project\数据采集与可视化课程\大作业\ajax\folk"
save_file_name = r'all.csv'

# 修改当前工作目录
os.chdir(folder_path)

# 将该文件夹下的所有文件名存入一个列表
file_list = [f for f in os.listdir() if f.endswith('.csv')]

# 读取第一个CSV文件并包含表头
df = pd.read_csv(os.path.join(folder_path, file_list[0]), encoding="utf_8_sig")

# 将读取的第一个CSV文件写入合并后的文件保存
df.to_csv(os.path.join(save_file_path, save_file_name), encoding="utf_8_sig", index=False)

# 循环遍历列表中各个CSV文件名，并追加到合并后的文件
for file in file_list[1:]:
    try:
        df = pd.read_csv(os.path.join(folder_path, file), encoding="utf_8_sig")
        df.to_csv(os.path.join(save_file_path, save_file_name), encoding="utf_8_sig", index=False, header=False, mode='a+')
    except Exception as e:
        print(f"Error reading {file}: {e}")

# 读取合并后的CSV文件
df = pd.read_csv(os.path.join(save_file_path, save_file_name), encoding="utf_8_sig")

# 删除重复数据
df.drop_duplicates(subset=['微博内容'], inplace=True, keep='first')

# 再次保存清洗后的CSV文件
df.to_csv(os.path.join(save_file_path, save_file_name), index=False, encoding='utf_8_sig')

print('合并完成')
