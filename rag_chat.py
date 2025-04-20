import os
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()

def load_llm():
    return Ollama(model="llama3.2:3b",base_url="http://host.docker.internal:11434",temperature=0.7)

def embed_and_store(transcribed_text):
    if not transcribed_text.strip(): 
        st.error("No content to process. Please check your PDF or input text.")
        return None 
    
    splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=100)
    documents = splitter.create_documents([transcribed_text])
    if not documents:
        st.error("No documents generated from the input. Please check the content.")
        return None

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
    )
    db = FAISS.from_documents(documents,embeddings)
    return db

def rag(combined_transcript):
    db = embed_and_store(combined_transcript)
    if db is None:
        return None
    retriever = db.as_retriever()
    llm = load_llm()
    st.session_state.qa_chain = RetrievalQA.from_chain_type(
        llm=llm,retriever=retriever,chain_type="stuff"
    )
    return retriever