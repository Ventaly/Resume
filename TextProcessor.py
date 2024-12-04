import os
import re
import shutil
import chardet
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
# 文本处理类
class TextProcessor:
    @staticmethod
    def clean_text(text):

        # 替换多余的空格
        cleaned_text = re.sub(r'\s+', ' ', text)
        # 替换多余的换行符
        cleaned_text = re.sub(r'\n+', '\n', cleaned_text)
        # 替换全角空格为半角空格
        cleaned_text = re.sub(r'[\u3000]+', ' ', cleaned_text)
        # 去除特殊字符，保留字母、数字、中文、空格和基本标点符号
        cleaned_text = re.sub(r'[^\w\s\u4e00-\u9fa5，。？！“”‘’（）《》【】]', '', cleaned_text)

        return cleaned_text

    @staticmethod
    def get_text_chunks(text):
        # 文本分割的函数
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=2000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        print(chunks)
        return chunks