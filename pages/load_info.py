import streamlit as st
import os
import pdfplumber
import json
import st_pages

st.set_page_config(
    page_title='Load Info - Interview Bot', 
    page_icon='🧑‍💻'
)

st.header('Tell me about your upcoming interview... 💬', divider='rainbow')


st.sidebar.markdown('**This demo presented by:**')
st.sidebar.markdown('*University of Washington - Foster School of Business*')
st.sidebar.markdown('*:violet[Class of 2024 - MSIS Team [TBD]]*')

if os.path.isfile('info.json'): 
    st.success('Your information has been successfully recorded! Please choose interview type to continue...', icon="✅")

    if st.button('Mock Interview'): 
        st.switch_page('pages/interview.py')
    if st.button('Speculate Interview'): 
        st.switch_page('pages/sp_interview.py')

    st.divider()
    if st.button('🔄 Delete Info & Start New'): 
        if os.path.isfile('info.json'): 
            os.remove('info.json')
            st.rerun()
    
    with open('info.json') as f:
        info = json.load(f)

        st.subheader('Company Name:', divider='blue')
        st.text(info['company_name'])

        st.subheader('Company Description:', divider='blue')
        st.text(info['company_description'])

        st.subheader('Job Title:', divider='blue')
        st.text(info['job_title'])
        st.text('Technical?: ' + 'Yes' if info['job_tech'] else 'No')

        st.subheader('Job Description', divider='blue')
        st.text(info['job_description'])

        st.subheader('Extracted Resume', divider='blue')
        st.text(info['resume'])
    

else: 
    company_name = st.text_input('Company Name')
    company_description = st.text_area('Company Description (Optional)')

    job_title = st.text_input('Job Title')
    job_tech = st.checkbox('Is this job technical?')
    job_description = st.text_area('Job Description')

    resume = st.file_uploader('Please upload your resume', type='pdf', )

    if st.button('Submit'): 
        
        has_empty = False
        
        for ele in [company_name, job_title, job_description]: 
            if len(ele.strip()) == 0:
                has_empty = True

        if (resume is None) or has_empty: 
            st.error('At least one required field is empty, please revise...', icon="🚨")

        else:
            with st.spinner('Processing...'): 
                info = {}

                info['company_name'] = company_name
                info['company_description'] = company_description
                info['job_title'] = job_title
                info['job_tech'] = job_tech
                info['job_description'] = job_description

                with pdfplumber.open(resume) as pdf: 
                    resume_text = ''
                    for page in pdf.pages:
                        resume_text = resume_text + page.extract_text()
                info['resume'] = resume_text

                with open('info.json', 'w') as f:
                    json.dump(info, f, indent=4)
        
            st.rerun()
