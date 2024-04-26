import streamlit as st
import streamlit_chatbox as stc
import time
import api_request
import json
import os
import st_pages

st.set_page_config(
    page_title='Mock Interview - Interview Bot', 
    page_icon='🧑‍💻'
)

chat_box = stc.ChatBox()

# config sidebar
if st.sidebar.button('🔄 Restart'): 
    chat_box.reset_history()
    st.rerun()

bot_llm = st.sidebar.radio('Bot LLM: ', ['OpenAI GPT-4 Turbo', 'OpenAI GPT-3.5 Turbo'])

st.sidebar.markdown('**This demo presented by:**')
st.sidebar.markdown('*University of Washington - Foster School of Business*')
st.sidebar.markdown('*:violet[Class of 2024 - MSIS [TBD]]*')

# header
st.header('Mock Interview 🧑‍💻', divider='rainbow')

if not os.path.isfile('info.json'): 
    st.error('You have not load your information yet, please load your information first...', icon='🚨')
    st.page_link("pages/load_info.py", label="Click Me to load your information", icon="📝")

else: 
    with open('info.json') as f:
            info = json.load(f)

    llm_avatar = "assistant"
    p_avatar = "user"

    # initialize llm
    if bot_llm == 'OpenAI GPT-4 Turbo': 
        llm = api_request.RecruiterGPT(info)
        llm_avatar = 'avatar/recruiter.png'
    elif bot_llm == 'OpenAI GPT-3.5 Turbo': 
        llm = api_request.RecruiterGPT(info, is_4=False)
        p_avatar = 'avatar/interviewee.png'


    chat_box = stc.ChatBox(user_avatar=p_avatar, assistant_avatar=llm_avatar)
    chat_box.output_messages()

    def send_to_chat(user_query):
        if user_query is not None:
            chat_box.user_say(user_query)

        generator = llm.get_response(chat_box.history)
        elements = chat_box.ai_say(
            [
                stc.Markdown("thinking", in_expander=False,
                            expanded=False, title="answer"),
                stc.Markdown("", in_expander=False, title="references"),
            ]
        )
        time.sleep(0.3)
        text = ""
        for chunk in generator:
            buffer = chunk.choices[0].delta.content
            if buffer is not None: 
                text += buffer
            chat_box.update_msg(text, element_index=0, streaming=True)
        chat_box.update_msg(text, element_index=0, streaming=False, state="complete")

    if len(chat_box.history) == 0:
        send_to_chat(None)

    if st.button('Done with Interview'): 
        st.subheader("Here is your feedback of this interview")
        st.divider()
        advisor_llm = api_request.AdvisorGPT()
        st.write_stream(advisor_llm.get_feedback(chat_box.history))
    
    if user_query := st.chat_input('Input your response here.'):
        send_to_chat(user_query)