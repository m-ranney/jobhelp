from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import os

def save_uploaded_file(uploaded_file):
    try:
        with open(os.path.join('tmp',uploaded_file.name),'wb') as f:
            f.write(uploaded_file.getvalue())
        return True, os.path.join('tmp',uploaded_file.name)
    except Exception as e:
        print(e)
        return False, str(e)

def process_resume(resume_file):
    success, file_path_or_error_message = save_uploaded_file(resume_file)
    if not success:
        raise Exception('Error saving uploaded file: ' + file_path_or_error_message)
  
    # TODO: Convert the Streamlit UploadedFile object to a format usable by PyPDFLoader

    loader = PyPDFLoader(resume_file)
    pages = loader.load_and_split()

    chat = ChatOpenAI()
    embeddings = OpenAIEmbeddings()

    db = Chroma.from_documents(pages, embeddings)
    retriever = db.as_retriever()

    qa = RetrievalQA.from_chain_type(llm=chat, retriever=retriever)

    # TODO: Use the qa object to match the resume against the job description and generate results

    return results
