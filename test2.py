import os
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def preprocess_text(text):
    # 去除标点符号和特殊字符
    text = re.sub(r'[^\w\s]', '', text)
    return text


def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def calculate_tfidf_similarity(resume_text, required_keywords):
    corpus = [resume_text, ' '.join(required_keywords)]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity_score[0][0]


def extract_skills_regex(text, keywords):
    # 使用正则表达式提取技能关键词
    skills = set()
    for keyword in keywords:
        pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
        if pattern.search(text):
            skills.add(keyword.lower())
    return skills


def extract_education(text):
    # 简单的正则表达式提取教育背景
    education_pattern = r'\b(?:本科|硕士|博士)\s+学位\b'
    matches = re.findall(education_pattern, text, re.IGNORECASE)
    return set(matches)


def extract_experience(text):
    # 简单的正则表达式提取工作经验
    experience_pattern = r'(\d+)\s*年?\s*工作经验'
    matches = re.findall(experience_pattern, text, re.IGNORECASE)
    total_years = sum(int(year) for year in matches)
    return total_years


def hard_requirements_filter(resume_text, required_keywords):
    # 检查简历中是否包含所有必需的关键字
    resume_words = set(preprocess_text(resume_text).lower().split())
    missing_keywords = [keyword for keyword in required_keywords if keyword.lower() not in resume_words]

    if missing_keywords:
        print(f"缺少以下关键字: {missing_keywords}")
        return False

    return True


def main():
    # 职位的关键技能和要求
    required_keywords = [
        "python", "c++",
        "ai大模型微调", "训练", "算法",
        "model", "llm", "agent",
        "linux", "深度学习", "tensorflow", "pytorch",
        "自然语言处理", "nlp", "transformer", "gpt", "sft"
    ]

    resume_path = input("请输入简历文件路径: ")

    if not os.path.exists(resume_path):
        print("文件路径错误，请检查后重新输入。")
        return

    resume_content = preprocess_text(load_file(resume_path))

    # 硬性要求筛选
    if not hard_requirements_filter(resume_content, required_keywords):
        print("该候选人的简历不符合硬性要求。")
        return

    # 计算TF-IDF相似度
    tfidf_similarity = calculate_tfidf_similarity(resume_content, required_keywords)

    # 提取技能并计算交集
    resume_skills = extract_skills_regex(resume_content, required_keywords)
    job_desc_skills = set(required_keywords)
    matched_skills = resume_skills.intersection(job_desc_skills)
    skill_match_ratio = len(matched_skills) / max(len(job_desc_skills), 1)

    # 提取教育背景并计算交集
    resume_education = extract_education(resume_content)
    # 假设职位描述中的教育背景为空，可以根据需要添加具体要求
    job_desc_education = set()
    matched_education = resume_education.intersection(job_desc_education)
    education_match_ratio = len(matched_education) / max(len(job_desc_education), 1)

    # 提取工作经验并计算交集
    resume_experience = extract_experience(resume_content)
    # 假设职位描述中的工作经验为空，可以根据需要添加具体要求
    job_desc_experience = 0
    experience_match_ratio = resume_experience / max(job_desc_experience, 1)

    # 综合评分
    weights = {
        'tfidf': 0.4,
        'skills': 0.3,
        'education': 0.2,
        'experience': 0.1
    }
    overall_score = (
            weights['tfidf'] * tfidf_similarity +
            weights['skills'] * skill_match_ratio +
            weights['education'] * education_match_ratio +
            weights['experience'] * experience_match_ratio
    )

    print(f"\n简历与职位描述的TF-IDF相似度分数: {tfidf_similarity:.2f}")
    print(f"匹配到的技能: {matched_skills}")
    print(f"技能匹配比例: {skill_match_ratio:.2f}")
    print(f"匹配到的教育背景: {matched_education}")
    print(f"教育背景匹配比例: {education_match_ratio:.2f}")
    print(f"匹配到的工作经验: {resume_experience} 年")
    print(f"工作经验匹配比例: {experience_match_ratio:.2f}")
    print(f"综合评分: {overall_score:.2f}")

    if overall_score >= 0.6:
        print("该候选人的简历符合职位要求。")
    else:
        print("该候选人的简历不符合职位要求。")


if __name__ == "__main__":
    main()
