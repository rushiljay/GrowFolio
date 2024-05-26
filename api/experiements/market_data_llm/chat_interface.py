from langchain_groq import ChatGroq
import streamlit as st

st.title('🦜🔗 Quickstart App')

groq_api_key = st.sidebar.text_input('Groq API Key', type='password')

def generate_response(input_text):
    print(input_text)
    print(type(input_text))
    llm = ChatGroq(temperature=1, groq_api_key=groq_api_key)
    response = llm.invoke({"input": input_text})
    st.write(response['answer'])

with st.form('my_form'):
    text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
    submitted = st.form_submit_button('Submit')
    if not groq_api_key.startswith('gsk_'):
        st.warning('Please enter your Groq API key!', icon='⚠')
    if submitted and groq_api_key.startswith('gsk_'):
        generate_response(text)
