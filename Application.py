import json
import os

from validators.mac_address import pattern

from FileProcessor import FileProcessor
from QianfanAPI import QianfanAPI
from ResumeReader import ResumeReader
from Similarity import Similarity
from TextProcessor import TextProcessor
from test import calculate_tfidf_similarity, extract_skills_bert, job_desc_content

class Application:
    def __init__(self, dir_name, file_path, json_path, pattern,required_keywords):
        self.dir_name = dir_name
        self.file_path = file_path
        self.json_path = json_path
        self.pattern = pattern
        self.required_keywords= required_keywords
    # 输入参数
    def run(self):


        resumes = ResumeReader.read_resumes(self.dir_name)
        for resume_name, resume_content in resumes.items():
            clean_text = TextProcessor.clean_text(resume_content)
            chunk_text = TextProcessor.get_text_chunks(clean_text)[0]
            tfidf_similarity = calculate_tfidf_similarity(resume_content, job_desc_content)
            a = ResumeReader.extract_skills_regex(chunk_text, self.required_keywords)
            print(a)
            skill_match_ratio =len(ResumeReader.extract_skills_regex(chunk_text,  self.required_keywords))/len( self.required_keywords)
            overall_score = (tfidf_similarity +skill_match_ratio)
            print(overall_score)
            if overall_score >=  0.50:
                print("简历初筛通过")

                job_text = ResumeReader.read_text(file_path)
                ner_text = QianfanAPI.background_qianfan(chunk_text, job_text)
                print(ner_text['result'])

                if "简历通过" in ner_text['result']:

                    pdf_path = os.path.join(self.dir_name, resume_name)
                    FileProcessor.process_pdf('简历筛选予以通过', pdf_path, self.dir_name)

                else:
                    print("淘汰")


            else:
                print("淘汰")


if __name__ == '__main__':
    dir_name = '../Resume_Data/Email-Attachments/Test_Resume/'
    file_path = os.path.join(dir_name, "岗位职责.txt")
    json_path = os.path.join(dir_name, "test.json")
    required_keywords = ["运维", "Linux", "Docker", "python", "shell", "K8S", ]
    # 用户输入部分
    # user_input = input("请输入所需的关键词（用逗号分隔）：")
    # required_keywords = [kw.strip() for kw in user_input.split(",")]
    pattern = r"总匹配度.*?(\d+%)"

    app = Application(dir_name, file_path, json_path, pattern)

    app.run()
