# encoding:utf-8
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model='qwen3.8-max', base_url='https://cn-beijing.maas.qianwenaiapi.com/compatible-mode/v1')

res = model.invoke(input="你好")

print(res.content, end='', flush=True)
