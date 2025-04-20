import streamlit as st
from src.audio_upload.audio_processing import audio_processing
from src.blog_url.blog_processing import blog_processing
from src.pdf_upload.pdf_processing import pdf_processing

def main():
    if "chat_history_audio" not in st.session_state:
        st.session_state.chat_history_audio = []
    if "chat_history_blog" not in st.session_state:
        st.session_state.chat_history_blog = []
    if "chat_history_pdf" not in st.session_state:
        st.session_state.chat_history_pdf = []

    st.set_page_config(page_title="RAG Chat",layout="centered")
    st.title("Content Summarizer")

    # Align radio buttons vertically within the column
    method = st.radio("Interact with",
    ["Audio File","Blog Url","Pdf File"]
    ,key="audio",horizontal=True)


    if method == "Audio File":
        audio_processing()
                        
    elif method == "Blog Url":
        blog_processing()
        
    elif method == "Pdf File":
        pdf_processing()
        

if __name__ == "__main__":
    main()


