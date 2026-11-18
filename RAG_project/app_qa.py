# encoding:utf-8
import time

import streamlit as st
from rag import RagService
import config_data as config

st.title("智能客服")
st.divider()  # 分隔符

if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "你好，有什么可以帮助你吗？"}]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 页面下方的输入栏
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    with st.spinner("AI思考中..."):
        stream_res = st.session_state["rag"].chain.stream({"input": prompt}, config.session_config)

        res = st.chat_message("assistant").write_stream(stream_res)

        st.session_state["message"].append({"role": "assistant", "content": res})
