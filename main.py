import streamlit as st
from langchain.schema import HumanMessage, AIMessage
from schema import app
import os

st.title("Chat with Swel Pay Lar")
st.write("မင်္ဂလာပါခင်ဗျ။ Swel Pay Lar - ဆွဲပေးလား မှ ကြိုဆိုပါတယ်။ ဘာများကူညီဆောင်ရွက်ပေးရမလဲခင်ဗျာ။")

if 'chat_history' not in st.session_state:
    st.session_state.msg_to_show = []
    st.session_state.chat_history=[]

st.write("")
final_text = ""

chat_text=st.chat_input("Enter Your Question...")

if st.session_state.msg_to_show:
    for msg in st.session_state.msg_to_show:
        st.chat_message('user').markdown(msg['human'])
        st.chat_message('assistant').markdown(msg['AI'])

if chat_text:
    final_text = chat_text

if final_text:
    st.chat_message('user').markdown(final_text)
    with st.spinner("Processing..."):
        result = app.invoke({'question': final_text, 'chat_history': st.session_state.chat_history})

    if result:
        st.chat_message('ai').markdown(result['response']['answer'])
        message = {'human': final_text, 'AI': result['response']['answer']}
        st.session_state.msg_to_show.append(message)

        st.session_state.chat_history.append(HumanMessage(content=final_text))
        st.session_state.chat_history.append(AIMessage(content=result['response']['answer']))


