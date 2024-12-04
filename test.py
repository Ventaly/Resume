import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline, BertTokenizer, BertForTokenClassification

resume_info = {
    "个人信息": {
        "姓名": "张振鹏",
        "性别": "男",
        "年龄": 29,
        "电话": "13453314213",
        "邮箱": "1131452116@qq.com",
        "现居住地": "深圳南山",
        "婚姻状况": "未婚",
        "最高学历": "本科",
        "工作年限": 7
    },
    "教育经历": [
        {
            "学校": "湖南人文科技学院",
            "专业": "物联网工程",
            "学位": "本科",
            "起止时间": "2014-01～2018-01"
        }
    ],
    "工作经历": [
        {
            "公司名称": "招联消费金融有限公司",
            "职位": "运维开发工程师",
            "工作时间": "2022-03～至今",
            "主要职责": ["""
                基于阿里腾讯华为 AWS谷歌微软云，python,搭建基于docker、k8s、自动化部署、CI/CD持续集成持续交付持续部署、微服务治理服务网格、应用管理、日志收集、监控告警系统、应用上云大力神器kubesphere等所有技术的完美平台。,
                监控巡检：告警列表、定时任务、资源使用率、健康检查（用户层、中后台层、基础设施层）、APM、数据库、Redis、依赖服务、应用日志等巡检,
                分析和处理用户事件单和IT问题，高可用演练：慢SQL、依赖服务、中间件、Redis、灰度切换、异地双活等演练,
                参与项目交付全生命周期：客户提出需求，BA和业务确认对其需求，产品开发，测试，运营和运维，后续的迭代和优化,
                负责Html Css Javascript React/Vue/angular Css框架/库 NodeJS/express Security Mongodb或Mysql/Postgresql REST/基本HTTP/应用层逻辑移至另一种后端语言（python或Java）和各自的Web框架（django/Flask或Spring）系统设计/网络架构和系统测试,
                负责网络、sql+plsql、数据结构+算法基础以及安全和系统设计,
                负责k8s容器编排技术和docker容器生产实践
                """
            ]
        },
        {
            "公司名称": "华为技术有限公司",
            "职位": "SRE运维开发工程师",
            "工作时间": "2017-07～2022-03",
            "主要职责": ["""
                负责开发，搭建平台，设计模块，优化产品，多线程并发编程，各种数据结构和算法，j2ee架构，Struts，Spring，Hibernate框架,
                负责Apache/Nginx/Tomcat，TCP/IP操作系统（Windows、Linux、IOS、Android等）,
                持续学习和掌握前沿合适技术：微服务架构、容器化部署等，并成功应用于项目中，提高开发效率和系统稳定性,
                高效完成中后台搭建和实现依赖服务高可用,
                通过分析系统和性能瓶颈，针对性进行优化：优化SQL、建立合适索引、去除冗余代码等
                """
            ]
        }
    ],
    "个人技能": [
        {"技能名称": "Android", "掌握程度": "未具体说明"},
        {"技能名称": "j2ee", "掌握程度": "一般"},
        {"技能名称": "Windows", "掌握程度": "未具体说明"},
        {"技能名称": "C/C++", "掌握程度": "一般"},
        {"技能名称": "Flask", "掌握程度": "基本"},
        {"技能名称": "Web", "掌握程度": "基本"},
        {"技能名称": "NodeJS", "掌握程度": "基本"},
        {"技能名称": "IOS", "掌握程度": "未具体说明"},
        {"技能名称": "Struts", "掌握程度": "一般"},
        {"技能名称": "DevOps", "掌握程度": "未具体说明"}
    ],
    "项目经历": []
}
job_desc_content="""

python， C++
AI大模型微调、训练  算法 


模型（LLM）Agent

Linux 深度学习 TensorFlow PyTorch
自然语言处理   NLP   Transformer   GPT  SFT
"""
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






def main():
    # 职位的关键技能和要求
    # 职位的关键技能和要求
    required_keywords = [
        "python", "c++",
        "ai大模型微调", "训练", "算法",
        "model", "llm", "agent",
        "linux", "深度学习", "tensorflow", "pytorch",
        "自然语言处理", "nlp", "transformer", "gpt", "sft"
    ]
    # 计算TF-IDF相似度

    for job in resume_info['工作经历']:

            for duty in job['主要职责']:
                print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                matched_skills = extract_skills_regex(duty, required_keywords)
                matched_skills = extract_skills_regex(duty, required_keywords)

                tfidf_similarity = calculate_tfidf_similarity(duty, job_desc_content)

                # 提取技能并计算交集
                # resume_skills = extract_skills_bert(duty)
                # job_desc_skills = set(required_keywords)
                # matched_skills = resume_skills.intersection(job_desc_skills)  # 计算技能交集
                skill_match_ratio = len(matched_skills) / max(len(required_keywords), 1)  # 计算技能匹配比例

                # 综合评分
                overall_score = (tfidf_similarity + skill_match_ratio) / 2  # 计算综合评分

                # 打印结果
                print(f"\n简历与职位描述的TF-IDF相似度分数: {tfidf_similarity:.2f}")
                print(f"匹配到的技能: {matched_skills}")
                print(f"技能匹配比例: {skill_match_ratio:.2f}")
                print(f"综合评分: {overall_score:.2f}")


if __name__ == "__main__":
    main()