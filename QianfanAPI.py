import os
import re
import shutil
import chardet
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate

from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
import qianfan
# 千帆API类
class QianfanAPI:
    @staticmethod
    def chat_with_qianfan(chunk_text, file_path):
        # 使用千帆API进行聊天的函数
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
        # 岗位要求     到岗时间   分批次
        # 读取文件内容
        with open(file_path, "r", encoding='utf-8') as f:
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

        # 替换{data}占位符
        content = data_placeholder.format(data=data)

        # 初始化千帆聊天完成对象
        llm = qianfan.ChatCompletion()

        # 调用千帆API
        resp = llm.do(model="ERNIE-4.0-8K", messages=[
            {
                "role": "user",
                "content": content
            }
        ])

        return resp




    def ner_qianfan(chunk_text):
        # 使用千帆API进行聊天的函数
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


        data_placeholder = f"""
                        作为数据处理助手，您的任务是分析以下简历文本，并提取以下部分的信息：

                            1. 个人信息（姓名、联系方式、邮箱等）
                            2. 教育经历（学校、专业、学位、起止时间等）
                            3. 项目经历（项目名称、时间、角色、关键职责等）
                            4. 工作经历（公司名称、职位、工作时间、主要职责等）
                            5. 个人技能（技能名称、掌握程度等）
                            
                            请确保提取的信息准确无误，并以JSON格式返回结果。以下是简历的文本内容：

                        个人简历：{chunk_text}

                        #json格式输出示例
                        [
                        {{
                          "personal_info": {{
                            "name": "付尧全",
                            "contact": "13580785508",
                            "email": "309853534@qq.com"
                          }},
                          "education": [
                            {{
                              "school": "东莞理工学院",
                              "major": "通信工程",
                              "degree": "本科",
                              "start_date": "2012-09",
                              "end_date": "2016-06"
                            }}
                          ],
                          "work_experience": [
                            {{
                              "company": "百度在线网络技术（北京）有限公司",
                              "position": "软件工程师",
                              "start_date": "2016-07",
                              "end_date": "2018-06",
                              "responsibilities": "在这里插入主要职责描述"
                            }}
                          ],
                          "projects": [
                            {{
                              "name": "西江干线电子航道图工程",
                              "duration": "2022-01 - 至今",
                              "role": "工程师",
                              "responsibilities": "负责机房和服务器，存储资源，安全设备，网络设备的调研，撰写可研报告和汇报PPT等。"
                            }}
                          ],
                          "skills": [
                            {{
                              "name": "Python",
                              "level": "熟练"
                            }},
                            {{
                              "name": "Java",
                              "level": "熟练"
                            }},
                            {{
                              "name": "数据库管理",
                              "level": "中等"
                            }}
                          ]
                        }}
                        ]  
                        
                        
                        确保所有生成的内容都与给定的文本直接相关，生成的是有效的JSON格式，并且内容高质量、准确、详细。 
                    """

        # 替换{data}占位符
        content = data_placeholder

        # 初始化千帆聊天完成对象
        llm = qianfan.ChatCompletion()

        # 调用千帆API
        resp = llm.do(model="ERNIE-4.0-8K", messages=[
            {
                "role": "user",
                "content": content,
                "format": "json"
            }
        ])

        return resp

    # def Extract_Text_qianfan(chunk_text,job_text):
    #     # 使用千帆API进行聊天的函数
    #     """
    #         使用千帆API进行聊天完成的操作。
    #
    #         参数:
    #         file_path: str, 包含岗位要求与岗位描述的文件的路径。
    #         data_placeholder: str, 在聊天内容中替换{data}的字符串。
    #
    #         返回:
    #         resp: qianfan.ChatCompletion()的响应对象。
    #         """
    #     # 设置环境变量
    #     os.environ["QIANFAN_AK"] = "AsCXMx7DdStZ7e4aGRUJVlDU"
    #     os.environ["QIANFAN_SK"] = "mVjaTtP3rrEFL2HxirasowZjjByI6zLW"
    #
    #     data_placeholder = f"""
    #                         任务：技能匹配
    #
    #                         说明：请从提供的简历文本和职位要求文本中精确提取技能关键词，并细致评估简历中所述技能与职位要求中所需的技能之间的匹配程度。最终返回包含匹配技能列表及每个技能匹配程度（以百分比表示，范围从0%到100%）的详细报告。
    #
    #                         输入格式：
    #
    #                         简历文本：一段详细列出个人专业技能、教育背景、工作经验（但评估时仅关注技能部分）的简历文本。
    #                         职位要求文本：一段明确列出该职位所需技能、资格条件及职责的详细描述性文本。
    #                         指南：
    #
    #                             技能提取：
    #                                 在简历文本中，专注于明确提及的专业技能、软件操作能力、编程语言掌握情况、行业知识等，确保提取的技能关键词与职位要求紧密相关。
    #                                 从职位要求文本中详细提取关键技能需求，包括但不限于必备技能、优先技能等。
    #                             匹配评估：
    #                             比较简历中的技能与职位要求中的技能，评估它们之间的相似度、相关性及熟练程度。
    #                                 直接匹配的技能评估：
    #                                     当简历中明确提到的技能与职位要求完全一致时，初步给予较高的匹配程度（如80%-95%）。
    #                                     评估时还需考虑技能描述的详细程度。例如，如果简历中不仅提到掌握了某项技能，还详细描述了使用该技能完成的具体项目或任务，那么匹配程度可以相应提高。
    #                                 部分匹配的技能评估：
    #                                     当技能相关但不完全一致，或技能类别相同但具体技术有所不同时，需根据相关性给予中等匹配程度（如50%-75%）。
    #                                     评估时，重点考虑技能之间的重叠部分和差异点。如果差异点较小，且重叠部分对职位要求至关重要，那么匹配程度可以接近上限（如75%）。
    #                                     如果差异点较大，但重叠部分仍对职位要求有一定贡献，那么匹配程度可以接近下限（如50%）。
    #                                 未覆盖的技能评估：
    #                                     对于职位要求中有提及但简历中未覆盖的技能，需视情况给予低匹配程度（如0%-49%）或标记为不匹配。
    #                                     如果这些未覆盖的技能对职位要求至关重要，且没有其他可替代的技能来弥补这一缺陷，那么匹配程度应接近0%。
    #                                     如果这些未覆盖的技能对职位要求不是绝对必要，或者简历中有其他相关技能可以作为补充，那么可以根据情况给予一定的匹配程度（如0%-49%）。
    #                             忽略内容：
    #                                 忽略简历中的非技能相关信息，如个人简介、兴趣爱好、软实力（比如团队协作能力、沟通能力等）以及教育背景中的非专业技能课程。
    #                                 忽略职位要求中的非技能性要求，如学历、工作经验年限、特定认证等，除非这些要求与技能评估直接相关（例如，特定认证作为某技能水平的证明）。
    #                         岗位要求与岗位描述：{job_text}
    #
    #                         个人简历：{chunk_text}
    #                         示例：
    #
    #                             候选人：张翔
    #
    #                             匹配技能列表及匹配程度：
    #
    #                                     Java编程
    #
    #                                         简历描述：熟练掌握，用于后端服务设计与开发
    #                                         匹配程度：100%
    #                                         说明：完全符合职位要求，且有实际工作经验支撑。
    #
    #                                     Spring框架
    #
    #                                         简历描述：使用Spring Boot实现业务逻辑
    #                                         匹配程度：90%
    #                                         说明：使用了Spring Boot这一主流框架，符合职位要求，但未明确提及Spring整体框架。
    #                                     C++编程
    #
    #                                         简历描述：未提及
    #                                         匹配程度：0%
    #                                         说明：简历中未提及C++技能，不符合职位要求。
    #                                     MySQL数据库管理
    #
    #                                         简历描述：熟练使用MySQL进行数据存储与查询
    #                                         匹配程度：95%
    #                                         说明：有明确的MySQL使用经验，且参与数据库设计与优化。
    #                                     Python编程
    #
    #                                         简历描述：基础掌握
    #                                         匹配程度：60%
    #                                         说明：虽然为基础掌握，但可作为辅助技能使用，符合优先技能的要求。
    #                                     Docker容器化技术
    #
    #                                         简历描述：熟练掌握，用于微服务架构的部署与管理
    #                                         匹配程度：100%
    #                                         说明：熟练掌握且实际应用于微服务架构，符合优先技能的要求。
    #                                     Linux系统管理
    #
    #                                         简历描述：熟练使用Linux操作系统
    #                                         匹配程度：85%
    #                                         说明：熟练使用Linux，与职位要求的系统管理高度相关。
    #                                     Git版本控制
    #
    #                                         简历描述：精通，参与团队协作开发
    #                                         匹配程度：100%
    #                                         说明：精通Git，符合软件操作能力的要求。
    #                                     MongoDB
    #
    #                                         简历描述：熟悉
    #                                         匹配程度：50%
    #                                         说明：虽然未明确提及，但熟悉MongoDB有助于数据库管理和开发。
    #                                     Jenkins
    #
    #                                         简历描述：了解
    #                                         匹配程度：40%
    #                                         说明：了解Jenkins，对CI/CD流程有一定认识，但未深入使用。
    #                                     金融科技
    #
    #                                         简历描述：具备相关知识
    #                                         匹配程度：100%
    #                                         说明：在金融科技领域有实际工作经验，完全符合行业知识要求。
    #                                     大数据分析
    #
    #                                         简历描述：具备相关知识（虽未明确提及，但隐含在工作经验中）
    #                                         匹配程度：70%（基于工作经验推断）
    #                                         说明：工作经验中涉及后端服务设计与开发，可推断具备数据分析能力。
    #                             总匹配度：83%
    #                 """
    #
    #     # 替换{data}占位符
    #     content = data_placeholder
    #
    #     # 初始化千帆聊天完成对象
    #     llm = qianfan.ChatCompletion()
    #
    #     # 调用千帆API
    #     resp = llm.do(model="ERNIE-4.0-8K", messages=[
    #         {
    #             "role": "user",
    #             "content": content,
    #             "format": "json"
    #         }
    #
    #     ])
    #
    #
    #     return resp

    def background_qianfan(chunk_text, job_text):
        # 使用千帆API进行聊天的函数
        """
            使用千帆API进行聊天完成的操作。

            参数:
            file_path: str, 包含岗位要求与岗位描述的文件的路径。
            data_placeholder: str, 在聊天内容中替换{data}的字符串。

            返回:
            resp: qianfan.ChatCompletion()的响应对象。
            """
        # 设置环境变量
        # os.environ["QIANFAN_AK"] = "cq0dzKva6CPvxE3xBnWHW3Ux"
        # os.environ["QIANFAN_SK"] = "wQ2XF4MzonPDpBAPExOTPkREMRIXzL64"

        os.environ["QIANFAN_AK"] = "AsCXMx7DdStZ7e4aGRUJVlDU"
        os.environ["QIANFAN_SK"] = "mVjaTtP3rrEFL2HxirasowZjjByI6zLW"

        data_placeholder = f"""
                            任务：简历与职位要求技能匹配

                            说明：请从提供的简历文本和职位要求文本中精确提取技能关键词，并细致评估简历中所述技能与职位要求中所需的技能之间的匹配程度。最终返回每个技能匹配程度（以百分比表示，范围从0%到100%）及总匹配度。

                            输入格式：

                            简历文本：一段详细列出个人专业技能、教育背景、工作经验（但评估时仅关注技能部分）的简历文本。
                            职位要求文本：一段明确列出该职位所需技能、资格条件及职责的详细描述性文本。
                            指南：

                                技能提取：
                                    在简历文本中，专注于明确提及的专业技能、软件操作能力、编程语言掌握情况、行业知识等，确保提取的技能关键词与职位要求紧密相关。
                                    从职位要求文本中详细提取关键技能需求，包括但不限于必备技能、优先技能等。
                                匹配评估：
                                比较简历中的技能与职位要求中的技能，评估它们之间的相似度、相关性及熟练程度。
                                    直接匹配的技能评估：
                                        当简历中明确提到的技能与职位要求完全一致时，初步给予80%的匹配度。这是基于技能名称的直接对应性给予的基准分。
                                        具体项目或任务描述：如果简历中不仅提到掌握了某项技能，还详细描述了使用该技能完成的具体项目或任务（包括项目规模、复杂度、候选人承担的角色、解决的问题等），那么匹配程度可以相应提高5%~10%。这反映了候选人在实际应用中的能力和经验。
                                        技能深度与广度：如果简历中展示了候选人在该技能领域的深度（如高级特性、性能优化等）和广度（如多种应用场景、与其他技能的结合等），也可以适当提高匹配程度。
                                    部分匹配的技能评估：
                                       当技能相关但不完全一致，或技能类别相同但具体技术有所不同时，需根据相关性给予中等匹配程度60%。这是基于技能之间的相似性给予的基准分。
                                        重叠部分的重要性：如果重叠部分对职位要求至关重要，且候选人在该部分有丰富经验和良好表现，那么匹配程度可以接近上限（如75%）。
                                        如果差异点较大，但重叠部分仍对职位要求有一定贡献，且候选人能够通过其他技能或经验来弥补这些差异点，那么匹配程度可以接近下限（如60%）。
                                    未覆盖的技能评估：
                                        对于职位要求中有提及但简历中未覆盖的技能，需视情况给予低匹配程度（如30%-49%）。
                                        至关重要且无可替代：如果这些未覆盖的技能对职位要求至关重要，且没有其他可替代的技能来弥补这一缺陷，那么匹配程度应接近0%。这反映了候选人在关键技能上的缺失和不符合职位要求的情况。
                                        非必要或有替代：如果这些未覆盖的技能对职位要求不是绝对必要，或者简历中有其他相关技能可以作为补充（即使这些替代技能不是完全相同的），那么可以根据情况给予一定的匹配程度（如0%-49%）。这考虑了候选人的整体能力和可能的替代方案。
                                    总匹配度计算：
                                        我们采用一种综合评估方式来确定总匹配度，即通过对各个技能匹配度进行累加，然后除以技能的总数。具体来说，计算公式为：总匹配度=各个技能匹配度之和/技能个数
                                        如果总匹配度，超过或者等于70%输出“简历通过”；如果总匹配度低于70%，则输出“简历不通过”
                                忽略内容：
                                    忽略简历中的非技能相关信息，如个人简介、兴趣爱好、软实力（比如团队协作能力、沟通能力等）以及教育背景中的非专业技能课程。
                                    忽略职位要求中的非技能性要求，如学历、工作经验年限、特定认证等，除非这些要求与技能评估直接相关（例如，特定认证作为某技能水平的证明）。
                            岗位要求与岗位描述：{job_text}

                            个人简历：{chunk_text}    
                            示例：

                                候选人：张翔

                                匹配技能列表及匹配程度：

                                        Java编程

                                            简历描述：熟练掌握，用于后端服务设计与开发，包括多线程处理、异常处理等。
                                            匹配程度：85%
                                            说明：完全符合职位要求，且有实际工作经验支撑，详细描述了技能的应用场景。
                                        Spring框架
                                        
                                            简历描述：使用Spring Boot实现业务逻辑，并熟悉Spring MVC和Spring Cloud等组件。
                                            匹配程度：90%
                                            说明：不仅使用了Spring Boot，还熟悉Spring整体框架的其他组件，高度符合职位要求。
                                        C++编程
                                        
                                                简历描述：未提及
                                                匹配程度：30%
                                                说明：简历中未提及C++技能。
                                        MySQL数据库管理
                                        
                                            简历描述：熟练使用MySQL进行数据存储与查询，包括索引优化、连表查询等高级操作。
                                            匹配程度：90%
                                            说明：有明确的MySQL使用经验，且参与数据库设计与优化，详细描述了技能的应用。
                                        Python编程
                                        
                                            简历描述：基础掌握，用于数据分析和脚本编写。
                                            匹配程度：70%
                                            说明：虽然为基础掌握，但已应用于数据分析和脚本编写，对职位要求有一定的贡献。
                                        Docker容器化技术
                                        
                                            简历描述：熟练掌握，用于微服务架构的部署与管理，包括Docker Compose和Kubernetes。
                                            匹配程度：85%
                                            说明：熟练掌握且实际应用于微服务架构，同时熟悉Docker Compose和Kubernetes，符合优先技能的要求。
                                        Linux系统管理
                                        
                                            简历描述：熟练使用Linux操作系统，包括系统配置、故障排查等。
                                            匹配程度：85%
                                            说明：熟练使用Linux，与职位要求的系统管理高度相关，详细描述了技能的应用。
                                        Git版本控制
                                        
                                            简历描述：精通，参与团队协作开发，使用Git进行代码管理、分支管理和合并冲突解决。
                                            匹配程度：90%
                                            说明：精通Git，详细描述了其在团队协作中的应用，符合软件操作能力的要求。
                                        MongoDB
                                        
                                            简历描述：熟悉MongoDB的基本操作和索引优化。
                                            匹配程度：70%
                                            说明：虽然未深入使用，但对MongoDB的基本操作和索引优化有了解，对数据库管理和开发有一定的贡献。
                                        Jenkins
                                        
                                            简历描述：了解Jenkins的基本配置和CI/CD流程。
                                            匹配程度：60%
                                            说明：对Jenkins和CI/CD流程有一定的认识，但未深入使用，匹配程度适中。
                                        金融科技
                                        
                                            简历描述：具备金融科技领域的实际工作经验，熟悉金融产品和业务流程。
                                            匹配程度：90%
                                            说明：在金融科技领域有实际工作经验，完全符合行业知识要求。
                                        大数据分析
                                        
                                            简历描述：在工作经验中涉及后端服务设计与开发，通过日志分析等方式支持大数据分析。
                                            匹配程度：75%
                                            说明：工作经验中隐含数据分析能力，虽然未明确提及，但可通过日志分析等方式支持大数据分析，对职位要求有一定的贡献。
                                总匹配度：76.6%，简历通过。
                                
                            确保所有生成的内容都与给定的文本直接相关，简历描述的内容是简历中的原话，不要编造简历中不存在的内容。总匹配度低于70%，请输出简历不通过，生成的格式请按照示例格式，最后单独输出总匹配度，严格按照准则进行评分审核。
                    """

        # 替换{data}占位符
        content = data_placeholder

        # 初始化千帆聊天完成对象
        llm = qianfan.ChatCompletion()

        # 调用千帆API
        resp = llm.do(model="ERNIE-4.0-8K", messages=[
            {
                "role": "user",
                "content": content,
                "format": "json"
            }

        ])

        return resp

    # def Extract_Text_qianfan(chunk_text):
    #     # 使用千帆API进行聊天的函数
    #     """
    #         使用千帆API进行聊天完成的操作。
    #
    #         参数:
    #         file_path: str, 包含岗位要求与岗位描述的文件的路径。
    #         data_placeholder: str, 在聊天内容中替换{data}的字符串。
    #
    #         返回:
    #         resp: qianfan.ChatCompletion()的响应对象。
    #         """
    #     # 设置环境变量
    #     os.environ["QIANFAN_AK"] = "AsCXMx7DdStZ7e4aGRUJVlDU"
    #     os.environ["QIANFAN_SK"] = "mVjaTtP3rrEFL2HxirasowZjjByI6zLW"
    #
    #     data_placeholder = f"""
    #                        作为数据处理助手，您的任务是分析以下简历文本，并提取以下部分的信息：
    #
    #                            1. 个人信息（姓名、联系方式、邮箱等）
    #                            2. 教育经历（学校、专业、学位、起止时间等）
    #                            3. 项目经历（项目名称、时间、角色、关键职责等）
    #                            4. 工作经历（公司名称、职位、工作时间、主要职责等）
    #                            5. 个人技能（技能名称、掌握程度等）
    #
    #                            请确保提取的信息准确无误，并以字符串格式返回结果。以下是简历的文本内容：
    #
    #                        个人简历：{chunk_text}
    #
    #                        #输出示例：
    #
    #                        [
    #                        {{
    #                          "personal_info": {{
    #                            "name": "付尧全",
    #                            "contact": "13580785508",
    #                            "email": "309853534@qq.com"
    #                          }},
    #                          "education": [
    #                            {{
    #                              "school": "东莞理工学院",
    #                              "major": "通信工程",
    #                              "degree": "本科",
    #                              "start_date": "2012-09",
    #                              "end_date": "2016-06"
    #                            }}
    #                          ],
    #                          "work_experience": [
    #                            {{
    #                              "company": "百度在线网络技术（北京）有限公司",
    #                              "position": "软件工程师",
    #                              "start_date": "2016-07",
    #                              "end_date": "2018-06",
    #                              "responsibilities": "在这里插入主要职责描述"
    #                            }}
    #                          ],
    #                          "projects": [
    #                            {{
    #                              "name": "西江干线电子航道图工程",
    #                              "duration": "2022-01 - 至今",
    #                              "role": "工程师",
    #                              "responsibilities": "负责机房和服务器，存储资源，安全设备，网络设备的调研，撰写可研报告和汇报PPT等。"
    #                            }}
    #                          ],
    #                          "skills": [
    #                            {{
    #                              "name": "Python",
    #                              "level": "熟练"
    #                            }},
    #                            {{
    #                              "name": "Java",
    #                              "level": "熟练"
    #                            }},
    #                            {{
    #                              "name": "数据库管理",
    #                              "level": "中等"
    #                            }}
    #                          ]
    #                        }}
    #                        ]
    #
    #
    #                        确保所有生成的内容都与给定的文本直接相关，生成的是有效的字符串格式,不包含分隔符，换行符，并且内容高质量、准确、详细。
    #                    """
    #
    #     # 替换{data}占位符
    #     content = data_placeholder
    #
    #     # 初始化千帆聊天完成对象
    #     llm = qianfan.ChatCompletion()
    #
    #     # 调用千帆API
    #     resp = llm.do(model="ERNIE-4.0-8K", messages=[
    #         {
    #             "role": "user",
    #             "content": content,
    #             "format": "json"
    #         }
    #
    #     ])
    #
    #     return resp