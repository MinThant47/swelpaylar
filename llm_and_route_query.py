from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from pydantic import BaseModel, Field
from typing import Literal
from langchain_google_genai import ChatGoogleGenerativeAI
import os

os.environ["GOOGLE_API_KEY"]= "AIzaSyC87rM9xeEqJ6Rt5LhguLed6QK5mzT6XBM"

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",
)


prompt = {
    'FAQ': ChatPromptTemplate.from_messages([
        ("system", """You are the chatbot for ဆွဲပေးလား - Swel Pay Lar Graphic Design Service.
        Your task is to respond to users in a friendly, fun, polite and informative manner.
        You have to provide information about frequently asked questions and general inquiries.
        for e.g. "Swel Pay Lar က ဘာလဲ" "ဘာဝန်ဆောင်မှုတွေရှိလဲ"
        Please only provide responses based on the context: {context}.
        Don't make up or change any information.
        If you don't find the related answer, just say "တောင်းပန်ပါတယ်။ လက်ရှိမှာ အဲ့မေးခွန်းအတွက် ပြင်ဆင်နေဆဲဖြစ်လို့ နောက်မှ ပြန်မေးပေးပါနော်။"
        But don't say words like according to provided text.
        Please reply only in BURMESE."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]),
     'Logo': ChatPromptTemplate.from_messages([
        ("system", """
        Your task is to respond to users in a friendly, fun, polite and informative manner.
        You have to provide information about Logo design related questions only based on the context: {context}.
        Don't make up or change any information.
        If you don't find the related answer, just say "တောင်းပန်ပါတယ်။ လက်ရှိမှာ အဲ့မေးခွန်းအတွက် ပြင်ဆင်နေဆဲဖြစ်လို့ နောက်မှ ပြန်မေးပေးပါနော်။"
        for e.g. "Logo fee တွေ ဘယ်လိုရှိလဲ" "Logo Package တွေက ဘာတွေလဲ"
        But don't say words like according to provided text.
        Please reply only in BURMESE."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]),
     'SocialAds': ChatPromptTemplate.from_messages([
        ("system", """
        Your task is to respond to users in a friendly, fun, polite and informative manner.
        You have to provide information about social meida design related questions only based on the context: {context}.
        Don't make up or change any information.
        for e.g. "Social ads fee တွေ ဘယ်လိုရှိလဲ" "Social media design Package တွေက ဘာတွေလဲ"
        If you don't find the related answer, just say "တောင်းပန်ပါတယ်။ လက်ရှိမှာ အဲ့မေးခွန်းအတွက် ပြင်ဆင်နေဆဲဖြစ်လို့ နောက်မှ ပြန်မေးပေးပါနော်။"
        But don't say words like according to provided text.
        Please reply only in BURMESE."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]),
     'Printing': ChatPromptTemplate.from_messages([
        ("system", """
        Your task is to respond to users in a friendly, fun, polite and informative manner.
        You have to provide information about printing design related questions only based on the context: {context}.
        Don't make up or change any information.
        for e.g. "Pamphlet Design တွေက ဘယ်လိုယူလဲ" "Pamphlet ဈေးဘယ်လိုယူလဲ" "Business Card Design ဆွဲပေးလား"
        If you don't find the related answer, just say "တောင်းပန်ပါတယ်။ လက်ရှိမှာ အဲ့မေးခွန်းအတွက် ပြင်ဆင်နေဆဲဖြစ်လို့ နောက်မှ ပြန်မေးပေးပါနော်။"
        But don't say words like according to provided text.
        Please reply only in BURMESE."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]),
    'Recommender': ChatPromptTemplate.from_messages([
        ("system", """ Your task is to respond to users in a friendly, fun, polite and informative manner.
        You are an intelligent assistant for social media ad packages consultation.
        Social Media Ad Packages: When a user asks about which social media ads package should they purchase, ask them questions like:
        "How many posts do you plan to publish per day/week?"
        Based on their answers, recommend the most suitable social media ad packages, taking into account their posting frequency.

        But don't say words like according to provided text.
        Please reply only in BURMESE"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]),
}

class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["FAQ", "Recommender", "Logo", "SocialAds", "Printing", "not_found"] = Field(
        ...,
        description="""You are given a user question, help me choose a route to
        FAQ or Recommender or not_found""",
    )

structured_llm_router = llm.with_structured_output(RouteQuery)

system = """You are an expert at routing a user question to FAQ or Recommender or not_found.
The FAQ contains about introdution, small talks, compliments and general frequently asked questions like Swel Pay Lar ဆိုတာ ဘာလဲ, ဘယ်လို service တွေရှိလဲ၊ revises ဘယ်နှခါပေးလဲ, contact info and payment methods
The Logo involves logo related question such as Logo Packages and logo design fees
The SocialAds involves social media (ads) design related question such as Social media Packages and fees
The Printing involves printing related question such as pamphlet or business card design fees.
The Recommender helps users what kind of social ads package they need.
If you can't find anything related to the above topics, then reply not_found
"""

route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)

question_router = route_prompt | structured_llm_router