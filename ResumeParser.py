# -*- coding: utf-8 -*-
import shutil
import chardet
from langchain.text_splitter import CharacterTextSplitter
import os
import  re
import qianfan
from PyPDF2 import PdfReader
#环境管理



# os.environ["OPENAI_API_TYPE"] = "azure"
# os.environ["OPENAI_API_VERSION"] = OPENAI_VERSION
# os.environ["AZURE_OPENAI_API_KEY"] = OPENAI_API_KEY
# os.environ["AZURE_OPENAI_ENDPOINT"] = OPENAI_BASE_URL
#load_dotenv()
# assistant_instructions = """
#  本助手将扮演一位求职者的角色，根据上传的pdf简历以及应聘工作的描述，来直接给HR写一个礼貌专业的求职新消息，要求能够用专业的语言结合简历中的经历和技能，并结合应聘工作的描述，来阐述自己的优势，尽最大可能打动招聘者。并且请您始终使用中文来进行消息的编写,开头是招聘负责人，结尾是真诚的，付尧全。这是一封完整的求职信，不要包含求职信内容以外的东西，例如“根据您上传的求职要求和个人简历，我来帮您起草一封求职邮件：”这一类的内容，以便于我直接自动化复制粘贴发送
# """

# 判断是否使用langchain。如果设置了自定义的api地址，则使用langchain
# def should_use_langchain():
#     should_use_langchain = OPENAI_BASE_URL is not None
#     return should_use_langchain


def read_pdf_content(pdf_path):
    """读取PDF文件的内容并返回。"""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() if page.extract_text else "" + "\n"
    return text
def read_resumes(directory_path):
    """遍历文件夹下的所有PDF简历文件并读取内容。"""
    resumes = {}
    # 遍历指定文件夹
    for filename in os.listdir(directory_path):
        # 检查文件是否为PDF文件
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(directory_path, filename)
            try:
                # 读取PDF文件内容
                content = read_pdf_content(pdf_path)
                resumes[filename] = content
            except Exception as e:
                print(f"无法读取文件 {filename}: {e}")
    return resumes


# 定义清理文本的函数
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

# 文本分割
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=2000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    print(chunks)
    return chunks

def chat_with_qianfan(chunk_text,file_path):
    """
    使用千帆API进行聊天完成的操作。

    参数:
    file_path: str, 包含岗位要求与岗位描述的文件的路径。
    data_placeholder: str, 在聊天内容中替换{data}的字符串。

    返回:
    resp: qianfan.ChatCompletion()的响应对象。
    """
    # 设置环境变量
    os.environ["QIANFAN_AK"] = "AsCXMx7DdStZ7e4aGRUJVlDU"
    os.environ["QIANFAN_SK"] = "mVjaTtP3rrEFL2HxirasowZjjByI6zLW"



    # 检测文件编码
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']

    # 使用检测到的编码打开文件
    with open(file_path, 'r', encoding=encoding) as f:
        content = f.read()
    #岗位要求     到岗时间   分批次
    # 读取文件内容
    with open(file_path, "r",encoding='utf-8') as f:
        data = f.read()
        data_placeholder = f"""
                作为招聘小助手，你的任务是协助企业进行智能化招聘。你需要从众多简历中筛选出优秀的候选人，对每个候选人进行评估，提高HR的工作效率与招聘质量。
                # 工具能力
                1.为了更精确地评估候选人的资格，采用分等级评分方法。评分标准包括但不限于：
                    教育背景：根据候选人的最高学历（本科、硕士、博士）以及毕业院校的排名（如985、211工程大学、一本、二本学院、大专院校）进行评分。
                    专业适配度：评估候选人的专业背景与岗位需求的契合程度。
                    工作经验年限：根据候选人工作经验的时间长度进行评分，以反映其对相关领域的熟悉程度。
                    项目经历：评估候选人参与的项目数量、规模以及相关性（关键词匹配），以判断其是否具备岗位所需的经验和技能。
                简历筛选具备智能筛选简历的能力，能够根据岗位描述和岗位要求，自动筛选出候选人是否符合条件（候选人必须有岗位的相关经验，否者直接不通过）。
                2. 按照岗位描述与要求和候选人的个人简历基本信息（技能匹配度、工作经验、教育背景、项目经历等其他相关标准）进行严格匹配，并对候选人进行打分。
                
                岗位要求与岗位描述：{data}
                
                个人简历：{chunk_text}

                #输出示例
                根据提供的岗位描述和岗位要求，以及张翔的简历内容，我将进行智能化筛选和评估：

                教育背景评分
                最高学历：硕士（上海海事大学软件工程）
                毕业院校排名：上海海事大学不属于985或211工程大学，但属于一本学院。
                评分：75/100（硕士学历加分，非985/211但为一本学院）
                专业适配度评分
                专业背景：软件工程，与岗位要求相关。
                评分：85/100（专业背景与岗位需求高度相关）
                工作经验年限评分
                工作经验：张翔有半年的量化实习经验。
                评分：60/100（实习经验虽与岗位不完全相关，但提供了一定的实践背景）
                项目经历评分
                项目经验：有基于知识图谱和知识库的大模型对话系统项目经验，与岗位要求相关。
                评分：75/100（项目经验与岗位需求相关，但缺乏行业应用经验）
                综合评分
                总分：75%（教育背景） + 85%（专业适配度） + 60%（工作经验年限） + 75%（项目经历） = 71.25/100
                评估结论
                简历通过：张翔的教育背景和专业适配度较高，项目经历也与岗位要求相关，尽管工作经验年限不足，但实习经验提供了一定的实践基础。因此，建议简历通过。
                简历通过

            """



    #替换{data}占位符
    content = data_placeholder.format(data=data)

    # 初始化千帆聊天完成对象
    llm = qianfan.ChatCompletion()

    # 调用千帆API
    resp = llm.do(model="ERNIE-4.0-8K",messages=[
        {
            "role": "user",
            "content": content
        }
    ])

    return resp


def process_pdf(review_result, pdf_path, new_folder):
    # 检查review_result是否包含特定文本
    if re.search(r'简历筛选予以通过', review_result):
        # 创建新文件夹（如果不存在）
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)

        # 将PDF文件移动到新文件夹
        shutil.move(pdf_path, os.path.join(new_folder, os.path.basename(pdf_path)))

        # 将review_result写入文本文件
        with open(os.path.join(new_folder, 'review_result.txt'), 'w', encoding='utf-8') as text_file:
            text_file.write(review_result)

# 另存文件夹
def process_pdf(review_result, pdf_path, base_folder):
        # 检查review_result是否包含特定文本
        if re.search(r'简历筛选予以通过', review_result):
            # 创建新文件夹（如果不存在）
            passed_folder = os.path.join(base_folder, "职位简历初筛通过")
            if not os.path.exists(passed_folder):
                os.makedirs(passed_folder)

            # 将PDF文件移动到新文件夹
            shutil.copy(pdf_path, os.path.join(passed_folder, os.path.basename(pdf_path)))
            print(f"文件已复制到 {passed_folder}")






if __name__ == '__main__':

    dir_name = '../Email-Attachments/11-05_职位：ai工程师'
    file_path = os.path.join(dir_name, "岗位职责.txt.txt")
    resumes =read_resumes(dir_name)
    for resume_name, resume_content in resumes.items():
        clean=clean_text(resume_content)
        chunk_text=get_text_chunks(clean)


        # 调用函数
        response = chat_with_qianfan(chunk_text,file_path)
        print(response)


        # 接收和处理响应
        review_result = response['result']
        print("审核结果：", review_result)
        # 示例使用
        if "简历通过" in review_result:




            pdf_path = os.path.join(dir_name, resume_name)  # 示例PDF文件路径


            process_pdf(review_result, pdf_path, dir_name)



    # 示例使用

    # pdf_path = 'path/to/your/resume.pdf'  # 替换为你的PDF文件路径
    # new_folder = 'path/to/new/folder'  # 替换为你想创建的新文件夹路径
    #
    # process_pdf(review_result, pdf_path, new_folder)