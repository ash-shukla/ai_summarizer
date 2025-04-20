import streamlit as st
from src.blog_url.extract_blog_content import extract_blog_content
from rag_chat import rag

def blog_processing():
    blog_url = st.text_input(label="Enter a blog url")
        
    if blog_url and "blog_processed" not in st.session_state:
        with st.spinner("Fetching blog url content..."):
            blog_content = extract_blog_content(blog_url)
            st.session_state.blog_content = blog_content
            st.session_state.blog_processed = True
            rag(blog_content)

    if st.session_state.get("blog_processed"):
        query = st.chat_input("Ask you question about the blog")
        if query and st.session_state.get("qa_chain"):
            with st.spinner("Thinking..."):
                answer = st.session_state.qa_chain(query)
                st.session_state.chat_history_blog.append(("user", query))
                st.session_state.chat_history_blog.append(("assistant", answer["result"] if isinstance(answer,dict) else answer))               

    if st.session_state.chat_history_blog:
        for role, text in st.session_state.chat_history_blog:
            st.chat_message(role).write(text)
