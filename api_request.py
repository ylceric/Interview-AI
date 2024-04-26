from openai import OpenAI
import streamlit as st

class RecruiterGPT:

    def __init__(self, info, is_4 = True): 
        self.init_prompt = f"""
            You are a top professional recruiter, you have been recruiter of companies like Apple, Google, Microsoft for past 10 years, now you are hired by {info['company_name']} as a recruiter, here is the company detail {info['company_description']}. Please ask interview question like a real HR. You will keep asking question and make it to be a conversation. You can also do follow up question based on user input. End the interview when you think it is a good. If you think interviewer did not explain well, let interviewer to give more specific example.  The interview steps are: 
            1. greeting
            2. personal introduction 
            3. 2-3 behavior question 
            4. if the job is related to technical, ask technical questions. If not related to technical, skip this step. 
            5. ask interviewer if they have any question. 

            Start interview question based on text delimited by <>.
            Text: <{info}>
            make it to be a conversation
            Start the interview now.
            """

        self.client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
        self.gpt_ver = 'gpt-4-turbo' if is_4 else 'gpt-3.5-turbo'
    
    def read_history(self, history): 
        messages = []
        messages.append({"role": "system", "content": self.init_prompt})

        for dict in history: 
            messages.append({
                'role': dict['role'], 
                'content': dict['elements'][0].content if dict['elements'] else ''
            })
        
        return messages

    def get_response(self, history):
        messages = self.read_history(history)
        
        stream = self.client.chat.completions.create(model=self.gpt_ver, messages=messages, stream=True)

        return stream
    
    

class AdvisorGPT:

    def __init__(self, is_4 = True): 
        self.init_prompt = f"""
            You are a top professional advisor, you have been recruiter of companies like Apple, Google, Microsoft for past 10 years. Now you have hired by university to evaluate student interview performance. The process is 
            1. give general feedback of only student performance about the whole interview. 
            2. for each student response, give some feedback and suggestion. 
            3. if the student response is bad, crate a better version based on that.  
            """

        self.client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
        self.gpt_ver = 'gpt-4-turbo' if is_4 else 'gpt-3.5-turbo'
    
    def read_history(self, history): 
        messages = []
        messages.append({"role": "system", "content": self.init_prompt})

        for dict in history: 
            messages.append({
                'role': dict['role'], 
                'content': dict['elements'][0].content if dict['elements'] else ''
            })
        
        return messages

    def get_feedback(self, history): 
        pre_messages = self.read_history(history)
        pre_text = ''

        for message in pre_messages: 
            pre_text = pre_text + 'role: ' + message['role'] + 'content: ' + message['content'] + '\n'
        
        messages = [{"role": "system", "content": f"Please give student feedback based on text delimited by <>.\n Text: <{pre_messages}>."}]

        stream = self.client.chat.completions.create(model=self.gpt_ver, messages=messages, stream=True)

        return stream

class IntervieweeGPT:

    def __init__(self, is_4 = True): 
        ## [TODO]
        self.init_prompt = f"""
            [TODO]
            """

        self.client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
        self.gpt_ver = 'gpt-4-turbo' if is_4 else 'gpt-3.5-turbo'
    
    def read_history(self, history): 
        messages = []
        messages.append({"role": "system", "content": self.init_prompt})

        for dict in history: 
            messages.append({
                'role': dict['role'], 
                'content': dict['elements'][0].content if dict['elements'] else ''
            })
        
        return messages

    def get_answer(self, history): 
        pre_messages = self.read_history(history)
        pre_text = ''

        for message in pre_messages: 
            pre_text = pre_text + 'role: ' + message['role'] + 'content: ' + message['content'] + '\n'
        
        messages = [{"role": "system", "content": f"[TODO]"}]

        stream = self.client.chat.completions.create(model=self.gpt_ver, messages=messages, stream=True)

        return stream