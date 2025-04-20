import os
import tempfile
import time
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader

def extract_pdf_content(pdf_file):
   with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as temp_pdf:
      temp_pdf.write(pdf_file.read())
      temp_path = temp_pdf.name   
    
   doc_loader = PyPDFLoader(temp_path)
   document = doc_loader.load() 

   os.remove(temp_path)
   content = "\n".join([doc.page_content for doc in document])
   st.toast("Fetching pdf content... please ask any question related to your file",icon="✅")
   time.sleep(1)
   return content.strip()
   
   