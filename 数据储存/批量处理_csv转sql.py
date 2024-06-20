import csv
import pymysql
import os

# 读取 CSV 文件并转换为 SQL 文件
def csv_to_sql(csv_file_path, table_name, sql_file_path):
    with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)

        with open(sql_file_path, 'w', encoding='utf-8') as sqlfile:
            sqlfile.write(f"CREATE TABLE IF NOT EXISTS `{table_name}` (\n")
            sqlfile.write(",\n".join([f"    `{header}` TEXT" for header in headers]))
            sqlfile.write("\n);\n\n")

            for row in reader:
                placeholders = ", ".join(["%s"] * len(row))
                values_tuple = tuple(row)
                sqlfile.write(f"INSERT INTO `{table_name}` ({', '.join([f'`{header}`' for header in headers])}) VALUES ({placeholders});\n")
                sqlfile.write(f"--VALUES--{values_tuple}\n")

# 执行 SQL 文件并存入 MySQL 数据库
def execute_sql_file(sql_file_path, db_config):
    conn = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        charset='utf8mb4'  # Ensure proper encoding
    )
    cursor = conn.cursor()

    with open(sql_file_path, 'r', encoding='utf-8') as sqlfile:
        sql_script = sqlfile.read()

    sql_commands = sql_script.split(';')
    for command in sql_commands:
        command = command.strip()
        if '--VALUES--' in command:
            try:
                insert_command, values_str = command.split('--VALUES--')
                insert_command = insert_command.strip()
                values_tuple = eval(values_str.strip())  # 转换为元组
                cursor.execute(insert_command, values_tuple)
            except Exception as e:
                print(f"Error executing command: {command}\nError: {e}")
        elif command:
            try:
                cursor.execute(command)
            except Exception as e:
                print(f"Error executing command: {command}\nError: {e}")

    conn.commit()
    cursor.close()
    conn.close()

# 遍历文件夹中的所有 CSV 文件并处理
def process_all_csv_files_in_directory(directory_path, db_config):
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            csv_file_path = os.path.join(directory_path, filename)
            table_name = os.path.splitext(filename)[0]  # 使用文件名作为表名
            sql_file_path = os.path.join(directory_path, f"{table_name}.sql")
            csv_to_sql(csv_file_path, table_name, sql_file_path)
            execute_sql_file(sql_file_path, db_config)

# 配置数据库连接信息
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'dyx031029',
    'database': 'scraping'
}

# 处理指定文件夹中的所有 CSV 文件
directory_path = r'D:\python_project\数据采集与可视化课程\大作业\data'  # 替换为你的 CSV 文件夹路径
process_all_csv_files_in_directory(directory_path, db_config)
