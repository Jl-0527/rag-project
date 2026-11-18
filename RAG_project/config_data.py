# encoding:utf-8
md5_path = "./md5.text"

# Chroma
collection_name = "rag"
persist_directory = "./chroma_db"

# Spliter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", ".", "!", "?", "。", "！", "？", " ", "", ]
max_spliter = 1000

# Search
similarity_threshold = 1

# model
embedding_model_name = 'text-embedding-v4'
chat_model_name = "qwen3.8-max"
model_base_url = 'https://cn-beijing.maas.qianwenaiapi.com/compatible-mode/v1'

# id
session_config = {
    "configurable": {
        "session_id": "user_001"
    }
}
