import os
import pandas as pd

# 读取CSV文件
csv_file_path = "data/txtfile2company.csv"
txt_folder_path = "data/pdf2txt"

# 读取CSV文件到DataFrame
df = pd.read_csv(csv_file_path, header=None, names=["index", "file_name", "company_name"])

# 遍历每一行，进行文件重命名
for _, row in df.iterrows():
    old_file_name = row["file_name"]
    company_name = row["company_name"]

    # 构建原始文件路径
    old_file_path = os.path.join(txt_folder_path, old_file_name)

    # 构建新的文件名（添加 .txt 扩展名）
    new_file_name = company_name + ".txt"
    new_file_path = os.path.join(txt_folder_path, new_file_name)

    # 重命名文件
    try:
        os.rename(old_file_path, new_file_path)
        print(f"已重命名: {old_file_name} -> {new_file_name}")
    except FileNotFoundError:
        print(f"未找到文件: {old_file_name}")
    except Exception as e:
        print(f"重命名文件 {old_file_name} 时出错: {e}")
