import streamlit as st
from src.blog_url.extract_blog_content import extract_blog_content
from generate_transcript import generate_transcript
from rag_chat import rag
import time

def main():
    if "chat_history_audio" not in st.session_state:
        st.session_state.chat_history = []
    if "chat_history_blog" not in st.session_state:
        st.session_state.chat_history_blog = []
    if "chat_history_pdf" not in st.session_state:
        st.session_state.chat_history_pdf = []

    st.set_page_config(page_title="RAG Chat",layout="centered")
    st.title("Yet to be decided")

    # Align radio buttons vertically within the column
    method = st.radio("Interact with",
    ["Audio File","Blog Url","Pdf File"]
    ,key="audio",horizontal=True)


    if method == "Audio File":
        uploaded_file = st.file_uploader("Please upload an audio",type=["mp3","m4a","wav"])
        if uploaded_file and ("audio_processed" not in st.session_state
            or st.session_state.get("last_uploaded_file_name") != uploaded_file.name
            ):
                with st.spinner("Loading Transcription..."):
                    transcription = generate_transcript(uploaded_file)
                    st.session_state.transcription_result = transcription
                    st.session_state.audio_processed = True
                    st.session_state.last_uploaded_file_name = uploaded_file.name

                    rag(transcription)
        
        if st.session_state.get("transcription_result"):
            st.subheader("Transcription Result:")
            st.markdown(f"```\n{st.session_state.transcription_result}\n```")
                    
        if st.session_state.get("audio_processed"):
            query = st.chat_input("Ask questions about the transcript")
            if query and st.session_state.get("qa_chain"):
                with st.spinner("Thinking..."):
                    answer = st.session_state.qa_chain(query)
                    
                    if isinstance(answer, dict) and "result" in answer:
                        st.write(answer["result"])  
                    else:
                        st.write(answer)
                        
    elif method == "Blog Url":
        blog_url = st.text_input(label="Enter a blog url")
        if blog_url and "blog_processed" not in st.session_state:
            with st.spinner("Fetching blog url content"):
                blog_content = extract_blog_content(blog_url)
                st.session_state.blog_content = blog_content
                st.session_state.blog_processed = True
                st.toast("Blog fetched successfully, please ask any question related to the blog",icon="✅")
                time.sleep(1)
                rag(blog_content)
        
        # if st.session_state.get("blog_content"):
        
        if st.session_state.get("blog_processed"):
            for role, text in st.session_state.chat_history_blog:
                st.chat_message(role).write(text)

            query = st.chat_input("Ask you question about the blog")
            if query and st.session_state.get("qa_chain"):
                with st.spinner("Thinking..."):
                    answer = st.session_state.qa_chain(query)
                    # st.write(answer["result"] if isinstance(answer,dict) else answer)
                    st.session_state.chat_history_blog.append(("user", query))
                    st.session_state.chat_history_blog.append(("assistant", answer["result"] if isinstance(answer,dict) else answer))               
                    
        for role, text in st.session_state.chat_history_blog:
            st.chat_message(role).write(text)

    elif method == "Pdf File":
        st.file_uploader("Upload a pdf file", type=["pdf"])


if __name__ == "__main__":
    main()


