import streamlit as st
import streamlit_chatbox as stc
import time
import api_request

st.set_page_config(
    page_title='Speculate Interview - MockView', 
    page_icon='🧑‍💻'
)

chat_box = stc.ChatBox()

# config sidebar
if st.sidebar.button('🔄 Restart'): 
    chat_box.reset_history()
    st.rerun()

bot_llm = st.sidebar.radio('LLM: ', ['OpenAI GPT-4 Turbo', 'OpenAI GPT-3.5 Turbo'])
st.sidebar.divider()

# header
st.header('Speculate Interview 👀', divider='rainbow')

if 'info' not in st.session_state: 
    st.error('You have not load your information yet, please load your information first...', icon='🚨')
    st.page_link("pages/load_info.py", label="Click Me to load your information", icon="📝")

    st.sidebar.markdown('**This demo presented by:**')
    st.sidebar.markdown('*University of Washington - Foster School of Business*')
    st.sidebar.markdown('*:violet[Class of 2024 - MSIS MaLou]*')

else: 
    is_over = True

    info = st.session_state['info']
    
    st.sidebar.subheader('Company & Job Info')
    st.sidebar.markdown('**Company:** ' + info['company_name'])
    st.sidebar.markdown('**Job Title:** ' + info['job_title'])
    st.sidebar.divider()
    if st.sidebar.button('Done with Interview'): 
        st.subheader("Here is your feedback of this interview")
        st.divider()
        advisor_llm = api_request.AdvisorGPT()
        st.write_stream(advisor_llm.get_feedback(chat_box.history))
        is_over = True
    st.sidebar.divider()

    st.sidebar.markdown('**This demo presented by:**')
    st.sidebar.markdown('*University of Washington - Foster School of Business*')
    st.sidebar.markdown('*:violet[Class of 2024 - MSIS MaLou]*')

    llm_avatar = 'avatar/recruiter.png'
    p_avatar = 'avatar/interviewee.png'

    # initialize llm
    if bot_llm == 'OpenAI GPT-4 Turbo': 
        llm = api_request.RecruiterGPT(info)
        llm_p = api_request.IntervieweeGPT(info)
    elif bot_llm == 'OpenAI GPT-3.5 Turbo': 
        llm = api_request.RecruiterGPT(info, is_4=False)
        llm_p = api_request.IntervieweeGPT(info, is_4=False)


    
    if st.button('Start Generating'): 
        is_over = False
    
    chat_box = stc.ChatBox(user_avatar=p_avatar, assistant_avatar=llm_avatar)
    chat_box.output_messages()

    while not is_over: 
        def send_to_chat(user_query_gen):
            global is_over

            if user_query_gen is not None:
                elements = chat_box.user_say(
                    [
                        stc.Markdown("thinking", in_expander=False,
                                    expanded=False, title="answer"),
                        stc.Markdown("", in_expander=False, title="references"),
                    ]
                )
                time.sleep(0.3)
                text = ""
                for chunk in user_query_gen:
                    buffer = chunk.choices[0].delta.content
                    if buffer is not None: 
                        text += buffer
                    chat_box.update_msg(text, element_index=0, streaming=True)
                chat_box.update_msg(text, element_index=0, streaming=False, state="complete")

            if len(chat_box.history):
                if chat_box.history[-1]['elements'][0].content == 'done':
                    is_over = True

            if not is_over:
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
        
        send_to_chat(llm_p.get_answer(chat_box.history))
    
    if len(chat_box.history) != 0:
        st.success('Interview Ended', icon='✅')

        st.subheader("Here is your feedback of this interview")
        st.divider()
        advisor_llm = api_request.AdvisorGPT()
        st.write_stream(advisor_llm.get_feedback(chat_box.history))
