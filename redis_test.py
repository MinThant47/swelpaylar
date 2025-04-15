from upstash_redis import Redis
import json

redis = Redis(url="https://boss-glider-21245.upstash.io", token="AVL9AAIjcDEzMzE4ZDE0NDRkYjM0ODFjODUzNzM3OWI3ZTBiODdjMnAxMA")

from langchain.schema import HumanMessage, AIMessage

# CHAT_KEY = "swel_pay_lar_chat_history"

def get_chat_key(user_id):
    return f"chat_history:{user_id}"

def save_chat_to_redis(chat_history, user_id):
    key = get_chat_key(user_id)
    serializable = [
        {"type": type(m).__name__, "content": m.content}
        for m in chat_history
    ]
    redis.set(key, json.dumps(serializable))

def load_chat_from_redis(user_id):
    key = get_chat_key(user_id)
    data = redis.get(key)
    if data:
        loaded = json.loads(data)
        history = []
        for msg in loaded:
            if msg["type"] == "HumanMessage":
                history.append(HumanMessage(content=msg["content"]))
            elif msg["type"] == "AIMessage":
                history.append(AIMessage(content=msg["content"]))
        return history
    return []

def clear_chat_from_redis(user_id):
    key = get_chat_key(user_id)
    redis.delete(key)