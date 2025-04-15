import streamlit as st
from streamlit_extras.bottom_container import bottom
from langchain.schema import HumanMessage, AIMessage
from schema import app
import os
from redis_test import load_chat_from_redis, save_chat_to_redis, clear_chat_from_redis

st.title("Chat with Swel Pay Lar")
st.write("မင်္ဂလာပါခင်ဗျ။ Swel Pay Lar - ဆွဲပေးလား မှ ကြိုဆိုပါတယ်။ ဘာများကူညီဆောင်ရွက်ပေးရမလဲခင်ဗျာ။")

from streamlit_cookies_controller import CookieController
import uuid

controller = CookieController()

cookies = controller.getAll()

user_id = controller.get("user_id")
st.write(user_id)

if user_id == "":
    user_id = str(uuid.uuid4())
    controller.set("user_id", user_id) 
    st.write("New User ID:" +user_id)

st.session_state.user_id = user_id


if 'chat_history' not in st.session_state:
    with st.spinner("Loading chat history..."):
        st.session_state.msg_to_show = []
        if user_id != "" and user_id != None:
            st.session_state.chat_history = load_chat_from_redis(user_id)

        history = st.session_state.chat_history
        for i in range(0, len(history), 2):
            if i+1 < len(history):
                st.session_state.msg_to_show.append({
                    'human': history[i].content,
                    'AI': history[i+1].content
                })

st.write("")
final_text = ""

with bottom():
    col1, col2 = st.columns([0.8,0.2])

    with col1:
        chat_text=st.chat_input("Enter Your Question...")

    with col2:
        if st.button("Clear Chat" ,type ="primary"):
            st.session_state.chat_history = []
            st.session_state.msg_to_show = []
            clear_chat_from_redis(user_id)

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
        save_chat_to_redis(st.session_state.chat_history, user_id)

