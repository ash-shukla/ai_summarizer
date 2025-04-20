import streamlit as st
from src.pdf_upload.extract_pdf_content import extract_pdf_content
from rag_chat import rag


def pdf_processing():
    uploaded_pdf_file = st.file_uploader("Upload a pdf file", type=["pdf"])
    if uploaded_pdf_file and "pdf_processed" not in st.session_state:
        with st.spinner("Fetching pdf content..."):
            pdf_content = extract_pdf_content(uploaded_pdf_file)
            st.session_state.pdf_processed = True
            st.session_state.pdf_content = pdf_content
            rag(pdf_content)
    
    if st.session_state.get("pdf_processed"):
        query = st.chat_input(f"Ask you question about your pdf file")
        if query and st.session_state.get("qa_chain"):
            with st.spinner("Thinking..."):
                answer = st.session_state.qa_chain(query)
                st.session_state.chat_history_pdf.append(("user", query))
                st.session_state.chat_history_pdf.append(("assistant", answer["result"] if isinstance(answer,dict) else answer)) 

    if st.session_state.get("pdf_processed") and st.session_state.chat_history_pdf: 
        for role, text in st.session_state.chat_history_pdf:
                st.chat_message(role).write(text)