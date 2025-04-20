import streamlit as st
from generate_transcript import generate_transcript
from rag_chat import rag

def audio_processing():
    uploaded_file = st.file_uploader("Please upload an audio",type=["mp3","m4a","wav"])
            # st.session_state.chat_history_audio = []
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
        st.markdown(
            f"<div style='white-space: pre-wrap; font-family: monospace;padding: 20px;'>{st.session_state.transcription_result}</div>",
            unsafe_allow_html=True
            )
                
    if st.session_state.get("audio_processed"):
        query = st.chat_input("Ask questions about the transcript")
        if query and st.session_state.get("qa_chain"):
            with st.spinner("Thinking..."):
                answer = st.session_state.qa_chain(query)
                st.session_state.chat_history_audio.append(("user", query))
                st.session_state.chat_history_audio.append(("assistant", answer["result"] if isinstance(answer,dict) else answer))               

    for role, text in st.session_state.chat_history_audio:
        st.chat_message(role).write(text)