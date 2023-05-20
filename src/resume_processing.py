from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from bs4 import BeautifulSoup
import requests
import os

def save_uploaded_file(uploaded_file):
    try:
        os.makedirs('tmp', exist_ok=True)  # create 'tmp' directory if it doesn't exist
        with open(os.path.join('tmp', uploaded_file.name),'wb') as f:
            f.write(uploaded_file.getvalue())
        return True, os.path.join('tmp', uploaded_file.name)
    except Exception as e:
        print(e)
        return False, str(e)

def process_resume(resume_file):
    success, file_path_or_error_message = save_uploaded_file(resume_file)
    if not success:
        raise Exception('Error saving uploaded file: ' + file_path_or_error_message)
  
    # Pass the file path to PyPDFLoader instead of the UploadedFile object
    loader = PyPDFLoader(file_path_or_error_message)

    # Split the resume
    resume_pages = loader.load_and_split()

    # Fetch the job description
    job_description_html = requests.get(job_url).text

    # Parse the HTML and extract the text
    soup = BeautifulSoup(job_description_html, 'lxml')
    job_description_text = soup.get_text()

    # TODO: Process the job description text (e.g., split into sections or paragraphs)

    chat = ChatOpenAI()
    embeddings = OpenAIEmbeddings()

    # Create Chroma databases for both the resume and job description
    resume_db = Chroma.from_documents(resume_pages, embeddings)
    job_description_db = Chroma.from_documents(job_description_text, embeddings)

    # Create RetrievalQA objects for both the resume and job description
    resume_qa = RetrievalQA.from_chain_type(llm=chat, retriever=resume_db.as_retriever())
    job_description_qa = RetrievalQA.from_chain_type(llm=chat, retriever=job_description_db.as_retriever())

    # TODO: Use the qa objects to match the resume against the job description and generate results
    # For now, we'll just return the resume and job description as they are
    results = {
        'resume': resume_pages,
        'job_description': job_description_text
    }

    return results