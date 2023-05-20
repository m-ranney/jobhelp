import streamlit as st
from src import resume_processing, cl_generation  # import the modules you created

def main():
    st.title('Job Application Assistant')

    st.subheader('Upload Your Resume')
    resume = st.file_uploader('Select a file', type='pdf')  # accepts pdf files

    st.subheader('Job Description')
    job_url = st.text_input('Enter the URL of the job description')

    st.subheader('Company Information')
    company_url = st.text_input('Enter the URL of the company')
    company_name = st.text_input('Enter the name of the company')

    if st.button('Generate Suggestions'):
        if resume is not None and job_url and company_url and company_name:
            results = resume_processing.process_resume(resume, job_url)
            # Display the contents of the resume and the job description
            st.write('Resume:')
            st.write(results['resume'])
            st.write('Job Description:')
            st.write(results['job_description'])
            st.success('Generated suggestions successfully!')
        else:
            st.error('Please fill in all fields')

if __name__ == '__main__':
    main()
