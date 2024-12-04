import re

class BackgroundScreen:

        def Screen(resume_data):

            experience=3
            # 检查教育背景是否为本科
            education_background = resume_data.get("education", [])
            education_background = resume_data.get("education", [])
            # 假设学历信息中的degree字段包含学历名称，如"Bachelor", "Master", "Doctor"
            has_bachelor_or_higher = any("本科" in item.get("degree", "").lower() or
                                         "硕士" in item.get("degree", "").lower() or
                                         "博士" in item.get("degree", "").lower() for item in education_background)
            # 计算各个公司工作时间累计之和
            work_experience = resume_data.get("work_experience", [])
            total_work_years = sum(int(re.search(r'(\d+)年', item.get("duration", "")).group(1)) for item in work_experience if
                                   re.search(r'(\d+)年', item.get("duration", "")))
            return  has_bachelor_or_higher and total_work_years > 3
