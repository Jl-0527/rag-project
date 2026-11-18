# encoding:utf-8
"""
知识库
"""
import hashlib
import os
import config_data as config
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime


def check_md5(md5_str: str):
    """检查传入的md5字符串是否已经被处理过
        return False(没有处理过)  True(已经处理过，有记录)
    """
    if not os.path.exists(config.md5_path):
        # if进入表示文件不存在，那么一定没有处理过
        with open(config.md5_path, 'w', encoding='utf-8') as f:
            pass
        return False
    else:
        with open(config.md5_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()  # 处理字符串前后的空格和回车
                if line == md5_str:
                    return True
        return False


def save_md5(md5_str: str):
    """将传入的md5字符串记录到文件里保存"""
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + "\n")


def get_string_md5(input_str: str, encoding='utf-8'):
    """将传入的字符串转换为md5字符串"""
    str_bytes = input_str.encode(encoding=encoding)

    md5_obj = hashlib.md5()  # 得到md5对象
    md5_obj.update(str_bytes)  # 更新内容
    md5_hex = md5_obj.hexdigest()  # 得到md5的十六进制字符串

    return md5_hex


class KnowledgeBaseService(object):
    def __init__(self):
        self.chroma = Chroma(
            collection_name=config.collection_name,  # 数据库表名
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory  # 数据库本地存储文件夹
        )  # 向量存储的实例 Chroma向量库对象

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,  # 分段最大长度
            chunk_overlap=config.chunk_overlap,  # 连续文本间的重叠数量
            separators=config.separators,  # 划分符号
            length_function=len  # 长度统计函数
        )  # 文本分类对象

    def upload_by_sty(self, data: str, filename):
        """将传入的字符串，进行向量化，存入向量数据库中"""
        md5_hex = get_string_md5(data)

        if check_md5(md5_hex):
            return "[跳过]已经存在"

        if len(data) > config.max_spliter:
            knowledge_chunks: list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "jihaohao"
        }

        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks]
        )

        save_md5(md5_hex)

        return "[成功]内容载入"


if __name__ == '__main__':
    knowledge = KnowledgeBaseService()
    r = knowledge.upload_by_sty("drt", "test")
    print(r)
