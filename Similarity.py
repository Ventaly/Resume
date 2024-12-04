import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"


from transformers import BertTokenizer, BertModel
from text2vec import SentenceModel

from text2vec import SentenceModel
import numpy as np

class Similarity:
    def calculate_cosine_similarity(text1, text2):
        # 加载模型
        model = SentenceModel('shibing624/text2vec-base-chinese')

        # 获取句子的嵌入表示
        sentences = [text1, text2]
        embeddings = model.encode(sentences)

        # 计算点积
        dot_product = np.dot(embeddings[0], embeddings[1])

        # 计算向量的范数
        norm_A = np.linalg.norm(embeddings[0])
        norm_B = np.linalg.norm(embeddings[1])

        # 计算余弦相似度
        cosine_similarity = dot_product / (norm_A * norm_B)

        return cosine_similarity

