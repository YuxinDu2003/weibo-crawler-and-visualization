import os
import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    data = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)

    with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

def convert_all_csv_in_folder(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            csv_file_path = os.path.join(folder_path, file_name)
            json_file_name = file_name.replace('.csv', '.json')
            json_file_path = os.path.join(folder_path, json_file_name)
            csv_to_json(csv_file_path, json_file_path)
            print(f'Converted {csv_file_path} to {json_file_path}')

# 指定文件夹路径
folder_path = r'D:\python_project\数据采集与可视化课程\大作业\data'
convert_all_csv_in_folder(folder_path)
