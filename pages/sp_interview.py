import streamlit as st
import streamlit_chatbox as stc
import api_request
import pandas as pd

st.set_page_config(
    page_title='Interview Bot', 
    page_icon='🧑‍💻'
)

chat_box = stc.ChatBox()

# config sidebar
if st.sidebar.button('🔄 New'): 
    chat_box.reset_history()
    st.rerun()

bot_llm = st.sidebar.radio('Bot LLM: ', ['OpenAI GPT-4 Turbo', 'OpenAI GPT-3.5 Turbo'])

st.sidebar.markdown('**This demo presented by:**')
st.sidebar.markdown('*University of Washington - Foster School of Business*')
st.sidebar.markdown('*:violet[Class of 2024 - MSIS [TBD]]*')

