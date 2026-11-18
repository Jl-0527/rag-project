# encoding:utf-8

from langchain_chroma import Chroma
import config_data as config


class VectorStoreSearchService(object):
    def __init__(self, embedding):
        """
        :param embedding:嵌入模型
        """
        self.embedding = embedding

        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory
        )

    def get_retriever(self):
        """返回向量检索器，方便入链"""
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_threshold})


if __name__ == '__main__':
    from langchain_community.embeddings import DashScopeEmbeddings

    retriever = VectorStoreSearchService(DashScopeEmbeddings(model="text-embedding-v4")).get_retriever()
    res = retriever.invoke("春天到了")
    for d in res:
        print(d.metadata)
