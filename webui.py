import streamlit as st
import st_pages

st.set_page_config(
    page_title='MockView', 
    page_icon='🧑‍💻'
)

# sidebar   
st_pages.show_pages([
    st_pages.Page('webui.py', 'About', '🏠'),
    st_pages.Page('pages/load_info.py', 'Load Info', '📝'),

    st_pages.Section('Interview'),
    st_pages.Page('pages/interview.py', 'Mock Interview', '▶️'), 
    st_pages.Page('pages/sp_interview.py', 'Speculate Interview', '▶️')
])

st.sidebar.markdown('**This demo presented by:**')
st.sidebar.markdown('*University of Washington - Foster School of Business*')
st.sidebar.markdown('*:violet[Class of 2024 - MSIS Team MaLou]*')


# main page
st.header('🧑‍💻 MockView', divider='rainbow')
st.subheader('💭 About this App')
st.subheader("**Redefining Interview Prep. Experience the AI Interview Assistant — Fair, Efficient, Personalized.**")


with st.expander('**🤖 🤖Simulate Reality:** AI vs AI mode lets you foresee your future performance.'): 
    st.markdown("Using our AI imitation function, based on your resume and constantly updated personal information, the AI can simulate your performance and conduct an interview. This will not only give you an idea of possible questions and your own response style before the interview, but it will also help you prepare and refine your interview strategies to better prepare for the actual interview.")

with st.expander('**🤔 📖Instant Feedback:** Immediate, clear advice to refine your skills.'): 
    st.markdown("Get real-time, clear advice right after your answers. Our AI analyzes your responses on the spot and provides actionable tips to refine your skills immediately—so every practice interview makes you sharper and more prepared.")

with st.expander('**✈️ 🌎Global Opportunities:** Prepare anywhere, anytime, for interviews worldwide.'): 
    st.markdown("We used our analytical skills and passion for technology to create this optimized AI-powered video interview software that makes the whole world your office. Wherever you are, you will have access to global career opportunities and be well prepared for them.")

st.subheader("**Simple, Intuitive, Effective** — Start your tailored practice sessions and approach every interview with confidence.")


st.header("▶️ Ready to Start?", divider='rainbow')
st.page_link("pages/load_info.py", label="Click Me to load your information", icon="📝")
