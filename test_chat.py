import streamlit as st
from streamlit_extras.bottom_container import bottom
from langchain.schema import HumanMessage, AIMessage
from schema import app
import os
from streamlit_cookies_controller import CookieController
import uuid
import time
from redis_test import load_chat_from_redis, save_chat_to_redis, clear_chat_from_redis

# Set the page configuration
st.set_page_config(page_title="Swel Pay Lar Chatbot", layout="centered")

# Add custom styles for chat UI
st.markdown("""
<style>

.st-key-orange button {
  background-color: #e58013 !important;
  color: white !important;
  padding: 0px 24px !important;
  font-weight: bold !important;
  box-shadow: none !important;
  outline: none !important;
}

.st-key-orange button:hover {
  background-color: #c66a05 !important;
  color: white !important;
  font-weight: bold !important;
  border: 1px solid rgba(0, 0, 0, 0.1) !important;
  box-shadow: none !important;
  outline: none !important;
}

.st-key-orange button:active, 
.st-key-orange button:focus,
.st-key-orange button:focus-visible {
  background-color: #c66a05 !important;
  color: white !important;
  font-weight: bold !important;
  border: 1px solid rgba(0, 0, 0, 0.1) !important;
  box-shadow: none !important;
  outline: none !important;
}

/* Additional global overrides */
.stButton button:focus {
  box-shadow: none !important;
  outline: none !important;
}

button:focus:not(:focus-visible) {
  box-shadow: none !important;
  outline: none !important;
}


  .message {
    max-width: 80%;
    padding: 15px 20px;
    border-radius: 20px 0px 20px 20px;
    font-size: 16.5px;
    line-height: 1.5;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    color: white;
    margin-bottom: 10px; /* Add margin-bottom to both user and bot messages */
  }

  .user-message {
    align-self: flex-end; /* Align the user message to the end */
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
  }

  .bot-message {
    background: linear-gradient(135deg, rgba(247, 148, 29, 0.25), rgba(247, 148, 29, 0.05));
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 15px 20px;
    border-radius: 0px 20px 20px 20px;
    font-size: 16.5px;
    line-height: 1.8;
    color: #f5f5f5;
    box-shadow: 0 8px 30px rgba(255, 128, 0, 0.1);
  }

  .chat-container {
    height: auto;
    padding: 10px 15px;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .bot-container {
    display: flex;
    align-items: flex-start;
    gap: 15px;
    overflow-wrap: break-word;
  }

  .bot-avatar {
    width: 30px;
    height: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .avatar-icon {
    margin-top: 10px;
    width: 35px;
    height: 35px;
  }

  .avatar-logo{
    width: 38px;
  }

  .st-emotion-cache-12cetgn {
    padding: 2rem 1rem !important;
}

.cls-1 {
    fill: url(#linear-gradient) !important;
    filter: url(#drop-shadow-1) !important;
}

</style>
""", unsafe_allow_html=True)


col1, col2 = st.columns([0.2, 0.8])

with col1:
  st.markdown("""
  <style>
  .logo {
  width: 7rem;
  }
  </style>
  <svg class="logo" id="Layer_1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 510.24 552.48"><defs><style>.cls-1{{fill:url(#linear-gradient);filter:url(#drop-shadow-1);}}</style><linearGradient id="linear-gradient" x1="12.19" y1="267.25" x2="480.1" y2="267.25" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#ff9f36"/><stop offset="1" stop-color="#f7941d"/></linearGradient><filter id="drop-shadow-1" x="0" y="0" width="510.24" height="552.48" filterUnits="userSpaceOnUse"><feOffset dx="9" dy="9"/><feGaussianBlur result="blur" stdDeviation="7"/><feFlood flood-color="#000" flood-opacity=".4"/><feComposite in2="blur" operator="in"/><feComposite in="SourceGraphic"/></filter></defs><path class="cls-1" d="M480.1,66.39l-38.56,30.2-2.87-9.57L59.47,12.12l420.62,54.27ZM258.81,294.48c-.88,9.96-9.05,17.94-19.03,18.56-.51.03-.94.05-1.32.05-11.27,0-20.44-9.17-20.44-20.44,0-.65.04-1.33.1-2.03.97-9.91,8.87-17.62,18.8-18.34l4.74-.34,170.32-166.17-269.61,68.74h0S12.19,207.7,12.19,207.7v54.05l26-5.05v-28.8l81.81-20.86v130.1c0,20.91-17.01,37.92-37.92,37.92h-43.88s0-47.08,0-47.08l57.09-10.99v-26.48l-83.09,15.99v94.57l69.89-.02c35.25,0,63.92-28.67,63.92-63.92v-136.72l178.36-45.47-94.34,92.04c-20.19,3.68-35.73,20.25-37.76,41.1-.15,1.54-.23,3.07-.23,4.56,0,25.61,20.83,46.44,46.44,46.44.93,0,1.91-.03,2.96-.1,20.95-1.31,38.42-16.9,42.54-37.12l96.22-93.88-46.04,180.58h-136.74c-35.25,0-63.92,28.67-63.92,63.92v69.89h193.37l21.19-83.04h-26.83l-14.55,57.04h-147.17v-43.89c0-20.91,17.01-37.92,37.92-37.92h156.94l73.88-289.78-169,164.89-.42,4.8Z"/></svg>""", unsafe_allow_html=True)
with col2:
  st.title("Chat with Swel Pay Lar")
  st.write("မင်္ဂလာပါခင်ဗျ။ Swel Pay Lar - ဆွဲပေးလား မှ ကြိုဆိုပါတယ်။ ဘာများကူညီဆောင်ရွက်ပေးရမလဲခင်ဗျာ။")

st.divider()

# # https://img.freepik.com/free-vector/abstract-perspective-grid-lines-black-background_1017-47349.jpg?t=st=1744909163~exp=1744912763~hmac=3718d67825ec737873be32ced8b8609c84ce208a263019ab4795e88ac4d479c3&w=826

# https://static.vecteezy.com/system/resources/thumbnails/002/704/174/small/dark-orange-smart-blurred-template-vector.jpg

st.markdown(
    f"""
    <style>
    .stApp {{
         background-image: url("https://media-hosting.imagekit.io/47867f8e1dde48d9/77928372_SL-072622-51930-16.jpg?Expires=1839562442&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=d4pSqUb-sFlpnzoBCSqnoNgHm7VA5Sem4UyGHdLnxZxNbQI154~OPCn76gzeClMmEm6u75A-BKNn9wYQ~u4AxhEdlxNtopaIVGKjka2Cv4thlXA637uK1bT6mQ4kcH49tNQ1PGdR8rMf3s04rF-ST4sartP~aEEJDLW9FthfStEoQ1RntifYz60I7dFcuc0mL~1qr5wGtNirUjLHidGYeFO41jnNBLEaPfTll6MQY0C9z4Hv~a6iinVILeBj~0c~NvJSUlLhiig2sYUyMf8S9ZaoK8HmcBT~4X4e1che0-AauApfa14Gj4iTAijsMyCjhJKPynzmep9W1k7ilyXN7w__");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# controller = CookieController()
# user_id = controller.get("user_id")

# # --- Session state setup
# if "initialized" not in st.session_state:
#     st.session_state.initialized = False
# if "cookie_check_start_time" not in st.session_state:
#     st.session_state.cookie_check_start_time = time.time()

# # --- Cookie waiting logic
# if not st.session_state.initialized:
#     if user_id is None:
#         elapsed = time.time() - st.session_state.cookie_check_start_time

#         if elapsed < 3:
#             st.write("⏳ Please wait...")
#             time.sleep(1)  # Give browser time to set cookie
#             st.rerun()
#         else:
#             # Still no cookie after 3 seconds – create a new user_id
#             user_id = str(uuid.uuid4())
#             controller.set("user_id", user_id)
#             st.session_state.user_id = user_id
#             st.session_state.initialized = True

#     elif user_id == "":
#         user_id = str(uuid.uuid4())
#         controller.set("user_id", user_id)
#         st.session_state.user_id = user_id
#         st.session_state.initialized = True

#     else:
#         st.session_state.user_id = user_id
#         st.session_state.initialized = True
# else:
#     user_id = st.session_state.user_id

# Cookie handling
controller = CookieController()

# --- Session state setup
if "initialized" not in st.session_state:
    st.session_state.initialized = False
if "cookie_check_start_time" not in st.session_state:
    st.session_state.cookie_check_start_time = time.time()

# Try to get the user_id cookie
try:
    user_id = controller.get("user_id")
except Exception:
    user_id = None

# --- Cookie waiting logic
if not st.session_state.initialized:
    if user_id is None:
        elapsed = time.time() - st.session_state.cookie_check_start_time

        if elapsed < 3:
            st.write("⏳ Please wait...")
            time.sleep(1)  # Give browser time to set cookie
            st.rerun()
        else:
            # Still no cookie after 3 seconds – create a new user_id
            user_id = str(uuid.uuid4())
            try:
                controller.set("user_id", user_id)
            except Exception:
                # Handle case where cookie can't be set
                pass
            st.session_state.user_id = user_id
            st.session_state.initialized = True

    elif user_id == "":
        user_id = str(uuid.uuid4())
        try:
            controller.set("user_id", user_id)
        except Exception:
            # Handle case where cookie can't be set
            pass
        st.session_state.user_id = user_id
        st.session_state.initialized = True

    else:
        st.session_state.user_id = user_id
        st.session_state.initialized = True
else:
    user_id = st.session_state.user_id

    
if 'chat_history' not in st.session_state:
    with st.spinner("Loading chat history..."):
        st.session_state.msg_to_show = []
        st.session_state.chat_history = []

        history = load_chat_from_redis(user_id)
        if history:
            st.session_state.chat_history = history
            for i in range(0, len(history), 2):
                if i + 1 < len(history):
                    st.session_state.msg_to_show.append({
                        'human': history[i].content,
                        'AI': history[i+1].content
                    })

# Create a chat input box
final_text = ""

with bottom():
    col1, col2 = st.columns([0.8, 0.2])

    with col1:
        chat_text = st.chat_input("Enter Your Question...")

    with col2:
        if st.button("Clear Chat", key="orange"):
            st.session_state.chat_history = []
            st.session_state.msg_to_show = []
            clear_chat_from_redis(user_id)

if st.session_state.msg_to_show:

    for msg in st.session_state.msg_to_show:
        st.markdown(f'<div class="chat-container"> <div class="message user-message">{msg["human"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bot-container"><div class="bot-avatar"><div class="avatar-icon"><svg class = "avatar-logo" id="Layer_1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 510.24 552.48"><defs><style>.cls-1{{fill:url(#linear-gradient);filter:url(#drop-shadow-1);}}</style><linearGradient id="linear-gradient" x1="12.19" y1="267.25" x2="480.1" y2="267.25" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#f8a746"/><stop offset="1" stop-color="#f7941d"/></linearGradient><filter id="drop-shadow-1" x="0" y="0" width="510.24" height="552.48" filterUnits="userSpaceOnUse"><feOffset dx="9" dy="9"/><feGaussianBlur result="blur" stdDeviation="7"/><feFlood flood-color="#000" flood-opacity=".4"/><feComposite in2="blur" operator="in"/><feComposite in="SourceGraphic"/></filter></defs><path class="cls-1" d="M480.1,66.39l-38.56,30.2-2.87-9.57L59.47,12.12l420.62,54.27ZM258.81,294.48c-.88,9.96-9.05,17.94-19.03,18.56-.51.03-.94.05-1.32.05-11.27,0-20.44-9.17-20.44-20.44,0-.65.04-1.33.1-2.03.97-9.91,8.87-17.62,18.8-18.34l4.74-.34,170.32-166.17-269.61,68.74h0S12.19,207.7,12.19,207.7v54.05l26-5.05v-28.8l81.81-20.86v130.1c0,20.91-17.01,37.92-37.92,37.92h-43.88s0-47.08,0-47.08l57.09-10.99v-26.48l-83.09,15.99v94.57l69.89-.02c35.25,0,63.92-28.67,63.92-63.92v-136.72l178.36-45.47-94.34,92.04c-20.19,3.68-35.73,20.25-37.76,41.1-.15,1.54-.23,3.07-.23,4.56,0,25.61,20.83,46.44,46.44,46.44.93,0,1.91-.03,2.96-.1,20.95-1.31,38.42-16.9,42.54-37.12l96.22-93.88-46.04,180.58h-136.74c-35.25,0-63.92,28.67-63.92,63.92v69.89h193.37l21.19-83.04h-26.83l-14.55,57.04h-147.17v-43.89c0-20.91,17.01-37.92,37.92-37.92h156.94l73.88-289.78-169,164.89-.42,4.8Z"/></svg></div></div><div class="message bot-message">{msg["AI"]}</div></div></div>', unsafe_allow_html=True)


if chat_text:
    final_text = chat_text

if final_text:
    st.markdown(f'<div class="chat-container"> <div class="message user-message">{final_text}</div>', unsafe_allow_html=True)

    with st.spinner("Processing..."):
        result = app.invoke({'question': final_text, 'chat_history': st.session_state.chat_history})

    if result:
        st.markdown(f'<div class="bot-container"><div class="bot-avatar"><div class="avatar-icon"><svg class ="avatar-logo" id="Layer_1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 510.24 552.48"><defs><style>.cls-1{{fill:url(#linear-gradient);filter:url(#drop-shadow-1);}}</style><linearGradient id="linear-gradient" x1="12.19" y1="267.25" x2="480.1" y2="267.25" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#f8a746"/><stop offset="1" stop-color="#f7941d"/></linearGradient><filter id="drop-shadow-1" x="0" y="0" width="510.24" height="552.48" filterUnits="userSpaceOnUse"><feOffset dx="9" dy="9"/><feGaussianBlur result="blur" stdDeviation="7"/><feFlood flood-color="#000" flood-opacity=".4"/><feComposite in2="blur" operator="in"/><feComposite in="SourceGraphic"/></filter></defs><path class="cls-1" d="M480.1,66.39l-38.56,30.2-2.87-9.57L59.47,12.12l420.62,54.27ZM258.81,294.48c-.88,9.96-9.05,17.94-19.03,18.56-.51.03-.94.05-1.32.05-11.27,0-20.44-9.17-20.44-20.44,0-.65.04-1.33.1-2.03.97-9.91,8.87-17.62,18.8-18.34l4.74-.34,170.32-166.17-269.61,68.74h0S12.19,207.7,12.19,207.7v54.05l26-5.05v-28.8l81.81-20.86v130.1c0,20.91-17.01,37.92-37.92,37.92h-43.88s0-47.08,0-47.08l57.09-10.99v-26.48l-83.09,15.99v94.57l69.89-.02c35.25,0,63.92-28.67,63.92-63.92v-136.72l178.36-45.47-94.34,92.04c-20.19,3.68-35.73,20.25-37.76,41.1-.15,1.54-.23,3.07-.23,4.56,0,25.61,20.83,46.44,46.44,46.44.93,0,1.91-.03,2.96-.1,20.95-1.31,38.42-16.9,42.54-37.12l96.22-93.88-46.04,180.58h-136.74c-35.25,0-63.92,28.67-63.92,63.92v69.89h193.37l21.19-83.04h-26.83l-14.55,57.04h-147.17v-43.89c0-20.91,17.01-37.92,37.92-37.92h156.94l73.88-289.78-169,164.89-.42,4.8Z"/></svg></div></div><div class="message bot-message">{result['response']['answer']}</div></div></div>', unsafe_allow_html=True)

        message = {'human': final_text, 'AI': result['response']['answer']}
        st.session_state.msg_to_show.append(message)

        st.session_state.chat_history.append(HumanMessage(content=final_text))
        st.session_state.chat_history.append(AIMessage(content=result['response']['answer']))
        save_chat_to_redis(st.session_state.chat_history, user_id)


st.write("")