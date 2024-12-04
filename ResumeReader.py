import os
import re
import shutil
import chardet
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline, BertTokenizer, BertForTokenClassification

# 简历阅读器类
class ResumeReader:

    @staticmethod
    def read_pdf_content(pdf_path):
        # 读取单个PDF文件内容的函数
        """读取PDF文件的内容并返回。"""
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() if page.extract_text else "" + "\n"
        return text

    @staticmethod
    def read_resumes(directory_path):
        # 读取PDF简历的函数
        """遍历文件夹下的所有PDF简历文件并读取内容。"""
        resumes = {}
        # 遍历指定文件夹
        for filename in os.listdir(directory_path):
            # 检查文件是否为PDF文件
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(directory_path, filename)
                try:
                    # 读取PDF文件内容
                    content = ""
                    for page in PdfReader(pdf_path).pages:
                        content += page.extract_text() if page.extract_text else "" + "\n"

                    resumes[filename] = content
                except Exception as e:
                    print(f"无法读取文件 {filename}: {e}")
        return resumes

    def read_text(directory_path):
        # 检测文件编码
        with open(directory_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']

        # 使用检测到的编码打开文件并读取内容
        with open(directory_path, 'r', encoding=encoding) as f:
            content = f.read()

        return content

    def extract_and_combine_experiences(resume_data):
        """
        从简历数据中提取工作职责和项目描述，并连接成一个字符串。

        参数:
        resume_data (dict): 简历的字典数据。

        返回:
        str: 包含所有工作职责和项目描述的字符串。
        """
        experiences_and_projects = []

        # 提取工作经历中的工作职责
        for job in resume_data.get("工作经历", []):
            responsibilities = job.get("工作职责", [])
            if isinstance(responsibilities, list):  # 确保工作职责是列表
                for responsibility in responsibilities:
                    experiences_and_projects.append(responsibility)
            else:
                experiences_and_projects.append(responsibilities)  # 单个字符串直接添加

        # 提取项目经验中的项目描述
        for project in resume_data.get("项目经验", []):
            project_description = project.get("项目描述", "")
            experiences_and_projects.append(project_description)

        # 将所有提取的信息连接成一个字符串
        experiences_and_projects_text = "\n".join(experiences_and_projects)
        return experiences_and_projects_text

    import re
    def extract_skills_regex(text, keywords):
        # 使用正则表达式提取技能关键词
        skills = set()
        for keyword in keywords:
            pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
            if pattern.search(text):
                skills.add(keyword.lower())
        return skills

    # 计算TF-IDF相似度的函数
    def calculate_tfidf_similarity(resume_text, job_desc_text):
        corpus = [resume_text, job_desc_text]  # 将简历和职位描述文本组成语料库
        vectorizer = TfidfVectorizer(stop_words='english')  # 初始化TF-IDF向量化器，去除英文停用词
        tfidf_matrix = vectorizer.fit_transform(corpus)  # 将文本转换为TF-IDF特征矩阵
        similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])  # 计算两个文本的余弦相似度
        return similarity_score[0][0]  # 返回相似度分数

    # 使用命名实体识别(NER)提取技能的函数
    def extract_skills_bert(text, model_name_or_path="../model/bert-base-chinese"):
        tokenizer = BertTokenizer.from_pretrained(model_name_or_path)
        model = BertForTokenClassification.from_pretrained(model_name_or_path)

        ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
        entities = ner_pipeline(text)

        skills = set([entity['word'] for entity in entities if entity['entity_group'] == '技能'])

        print(skills)

        return skills

    def extract_skills_regex(text, keywords):
        # 使用正则表达式提取技能关键词
        skills = set()
        for keyword in keywords:
            pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
            if pattern.search(text):
                skills.add(keyword.lower())
        return skills

    def extract_match_percentage(text, pattern):
        """
        从给定的文本中提取与正则表达式模式匹配的百分比。

        参数:
        text (str): 要搜索的文本。
        pattern (str): 用于匹配的正则表达式模式，其中应包含一个捕获组来捕获百分比。

        返回:
        str: 匹配的百分比，如果未找到匹配项则返回None。
        """
        match = re.search(pattern, text)
        if match:
            percent_str=match.group(1)
            print("percent_str:", percent_str)
            num_str = percent_str[:-1]
            # 将剩余的字符串转换为浮点数
            float_num = float(num_str)
            # 如果你想要得到实际的数值（即去掉百分比的百分比形式），你需要将浮点数除以100
            actual_num = float_num / 100
            return actual_num
        else:
            return None