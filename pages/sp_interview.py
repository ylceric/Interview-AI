import streamlit as st
import streamlit_chatbox as stc
import time
import api_request
import streamlit_scrollable_textbox as stx
import pandas as pd
import random
import os
import glob
import st_pages

st.set_page_config(
    page_title='Interview Bot', 
    page_icon='🧑‍💻'
)

chat_box = stc.ChatBox()

# config sidebar
if st.sidebar.button('🔄 New'): 
    chat_box.reset_history()
    st.rerun()
st_pages.show_pages([
    st_pages.Page('webui.py', 'About', '🏠'),
    st_pages.Page('pages/load_info.py', 'Load Info', '📝'),
    st_pages.Page('pages/interview.py', 'Mock Interview', '▶️'), 
    st_pages.Page('pages/sp_interview.py', 'Speculate Interview', '▶️')
])

bot_llm = st.sidebar.radio('Bot LLM: ', ['OpenAI GPT-4 Turbo', 'OpenAI GPT-3.5 Turbo'])

st.sidebar.markdown('**This demo presented by:**')
st.sidebar.markdown('*University of Washington - Foster School of Business*')
st.sidebar.markdown('*:violet[Class of 2024 - MSIS [TBD]]*')

