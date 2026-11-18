# RAG 智能问答项目

一个基于 LangChain、Streamlit 和 Chroma 的轻量级检索增强生成（RAG）示例。项目包含 TXT 知识库上传、向量检索、带本地对话历史的问答页面。

## 项目结构

```text
.
├── main.py                         # 独立聊天模型调用示例
├── README.md
├── .gitignore
└── RAG_project/
    ├── app_qa.py                   # Streamlit 智能问答页面
    ├── app_file_uploader.py        # Streamlit TXT 知识库上传页面
    ├── rag.py                      # RAG 问答链与提示词组装
    ├── knowledge_base.py           # 文本切块、去重和向量入库
    ├── vector_stores_search.py     # Chroma 向量检索
    ├── file_history_store.py       # 本地文件对话历史存储
    ├── config_data.py              # 模型、切块、向量库和会话配置
    └── data/                       # 示例知识文本
```

运行时会在 `RAG_project/` 下创建 `chroma_db/`、`chat_history/` 和 `md5.text`。这些本地数据不会提交到 Git。

## 工作流程

1. 上传页面读取 UTF-8 编码的 TXT 文件。
2. 知识库服务通过内容 MD5 跳过已导入文本，并将新文本切块、生成向量后写入 Chroma。
3. 问答页面根据问题从 Chroma 检索相关文本片段。
4. RAG 链将检索结果、对话历史和当前问题组合后交给聊天模型，并流式显示回答。

## 环境准备

需要 Python 3.10 或更高版本，以及可用的 DashScope API Key。项目通过 OpenAI 兼容接口调用 Qwen 聊天模型，并使用 DashScope Embeddings。

在项目根目录创建并启用虚拟环境后，安装依赖：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install streamlit langchain langchain-core langchain-openai langchain-community langchain-chroma langchain-text-splitters dashscope
```

配置 API Key（仅对当前 PowerShell 窗口生效）：

```powershell
$env:DASHSCOPE_API_KEY = "你的 DashScope API Key"
```

请勿将 API Key 写入源码或提交到 Git。

## 启动

从仓库根目录运行以下命令。配置中的数据库、历史记录和 MD5 文件路径是相对于当前工作目录的，因此需要先切换到 `RAG_project`：

```powershell
Set-Location .\RAG_project
streamlit run app_file_uploader.py
```

另开一个终端并同样进入 `RAG_project`，启动问答页面：

```powershell
Set-Location .\RAG_project
streamlit run app_qa.py
```

`main.py` 是不经过知识库的单次聊天模型调用示例，可从仓库根目录运行：

```powershell
python main.py
```

## 配置说明

主要配置位于 `RAG_project/config_data.py`，包括聊天模型、嵌入模型、Chroma collection 名称、文本切块长度、检索数量和会话 ID。当前会话 ID 固定为 `user_001`，多个用户部署时应改为每个用户独立的会话标识。
