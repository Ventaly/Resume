import os
import re
import shutil
import chardet
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
import  json


# 文件处理器类
class FileProcessor:
    @staticmethod
    def process_pdf(review_result, pdf_path, new_folder):
        # 处理PDF文件的函数
        # 检查review_result是否包含特定文本
        if re.search(r'简历筛选予以通过', review_result):
            # 创建新文件夹（如果不存在）
            passed_folder = os.path.join(new_folder, "职位简历初筛通过")
            if not os.path.exists(passed_folder):
                os.makedirs(passed_folder)

            # 将PDF文件移动到新文件夹
            shutil.copy(pdf_path, os.path.join(passed_folder, os.path.basename(pdf_path)))
            print(f"文件已复制到 {passed_folder}")

    def clean_json_string(data):

        # 检查字符串是否包含```和"json"
        # 清理字符串中的空格、反斜杠和换行符
        cleaned_str = data.replace('\\', '').replace('\n', '').replace(' ', '')

        print(cleaned_str)

        if '```' in data and 'json' in data:
            # 去掉前后的```和第一个"json"
            cleaned_data = data.strip()[3:-3].replace('json', '', 1)
            return cleaned_data
        else:
            # 如果不包含，返回原始数据
            return data

    def extract_responsibilities(data):
        """
        提取工作履历中的职责描述。

        参数:
        data (list): 包含个人简历信息的列表。

        返回:
        list: 包含所有工作履历职责描述的列表。
        """
        responsibilities_list = []

        # 遍历列表中的每个字典（每个字典代表一个人的简历信息）
        for person in data:
            # 获取 'work_experience' 列表
            work_experiences = person.get('work_experience', [])

            # 遍历 'work_experience' 列表
            for experience in work_experiences:
                # 获取 'responsibilities' 的值
                responsibilities = experience.get('responsibilities', '无')
                # 添加到列表中
                responsibilities_list.append(responsibilities)

        return responsibilities_list

    def write_json(data, file_path):
        """
        将数据写入 JSON 文件。

        参数:
        data (dict or list): 要写入文件的 Python 字典或列表。
        file_path (str): 要写入的 JSON 文件的路径。
        """
        data1=FileProcessor.clean_json_string(data)
        try:
            # 将数据写入 JSON 文件
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data1, file, ensure_ascii=False, indent=4)
                print()
            print(f"数据已成功写入 {file_path}")
        except Exception as e:
            print(f"写入文件时发生错误：{e}")

        # 从JSON文件导入数据
        with open(file_path, 'r', encoding='utf-8') as json_file:
            imported_data = json.loads(json_file)

        return imported_data
