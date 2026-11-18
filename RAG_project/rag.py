# encoding:utf-8
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from vector_stores_search import VectorStoreSearchService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from file_history_store import get_history


def print_prompt(prompt):
    print("==" * 20, prompt.to_string(), "==" * 20)
    return prompt


class RagService(object):
    def __init__(self):
        self.vector_service = VectorStoreSearchService(
            DashScopeEmbeddings(model=config.embedding_model_name)
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的参考资料为主，简洁专业的回答用户问题。参考资料：{context}"),
                ("system", "并且提供用户对话的历史记录如下："),
                MessagesPlaceholder("history"),
                ("user", "用户提问：{input}")
            ]
        )
        self.chat_model = ChatOpenAI(
            model=config.chat_model_name,
            base_url=config.model_base_url
        )
        self.chain = self.__get_chain()

    def __get_chain(self):
        """获得最终的执行链"""
        retriever = self.vector_service.get_retriever()

        def format_document(docs: list[Document]):
            if not docs:
                return "无参考资料"

            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"

            return formatted_str

        def format_for_retriever(value: dict) -> str:
            return value["input"]

        def format_for_prompt_template(value):
            # {input,context,history}
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["history"] = value["input"]["history"]
            return new_value

        chain = (
                {
                    "input": RunnablePassthrough(),
                    "context": RunnableLambda(format_for_retriever) | retriever | format_document
                } | RunnableLambda(format_for_prompt_template) | self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",  # 输入占位符
            history_messages_key="history"  # 输入占位符
        )
        return conversation_chain


if __name__ == '__main__':

    res = RagService().chain.invoke({"input": "春天适合穿什么"}, config.session_config)
    print(res)
