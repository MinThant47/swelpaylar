from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from pydantic import BaseModel, Field
from typing import Literal
from langchain_google_genai import ChatGoogleGenerativeAI
import os

try:
    os.environ["GOOGLE_API_KEY"]= "AIzaSyC87rM9xeEqJ6Rt5LhguLed6QK5mzT6XBM"
except:
    os.environ["GOOGLE_API_KEY"]= "AIzaSyBWn4Tay_jDvdtatWziBVxZ90DdoXGx5h8"


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
        DON'T INVENT OR CHANGE ANY INFORMATION, ESPECIALLY THE PRICING!

        If the user asks pricing questions (like "ဈေးနှုန်းက ဘာတွေလဲ" or "ဘယ်လောက်လဲ") or requests design samples (like "နမူနာပြပါ" or "sample design တွေပြပါ") and you don't have the specific context, respond with a follow-up question asking which specific service or design type they're interested in.

        For example:

        "ဘယ်ဒီဇိုင်းအမျိုးအစားရဲ့ ဈေးနှုန်းကို သိချင်တာပါလဲ? Logo, Social ads, Vinyl, Billboard, စသည်ဖြင့် အမျိုးအစားပေါ်မူတည်ပြီး ဈေးနှုန်းမတူညီပါ။"
        "ဘယ် Design နမူနာတွေကို ကြည့်ချင်တာလဲဗျ? Logo Design, Social ads, printing အမျိုးအစား အစုံရှိပါတယ်။"

        If you don't find the related answer, just say "တောင်းပန်ပါတယ်။ လက်ရှိမှာ အဲ့မေးခွန်းအတွက် ပြင်ဆင်နေဆဲဖြစ်လို့ Page CB မှာမေးပေးပါနော်။"
        But don't say words like according to provided text.
        Please reply only in BURMESE."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]),
     'Logo': ChatPromptTemplate.from_messages([
        ("system", """
        Your task is to respond to users in a friendly, fun, polite and informative manner.
        You have to provide information about Logo design related questions only based on the context: {context}.
        DON'TINVENT OR CHANGE ANY INFORMATION, ESPECIALLY THE PRICING!
        for e.g. "Logo fee တွေ ဘယ်လိုရှိလဲ" "Logo Package တွေက ဘာတွေလဲ"
        If you don't find the related answer, just say "တောင်းပန်ပါတယ်။ လက်ရှိမှာ အဲ့မေးခွန်းအတွက် ပြင်ဆင်နေဆဲဖြစ်လို့ Page CB မှာမေးပေးပါနော်။"
        But don't say words like according to provided text.
        Please reply only in BURMESE."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]),
     'SocialAds': ChatPromptTemplate.from_messages([
        ("system", """
        Your task is to respond to users in a friendly, fun, polite and informative manner.
        You have to provide information about social meida design/ sicuak related related questions only based on the context: {context}.
        DON'TINVENT OR CHANGE ANY INFORMATION, ESPECIALLY THE PRICING!
        for e.g. "Social ads fee တွေ ဘယ်လိုရှိလဲ" "Social media design package/ Social ads package တွေက ဘာတွေလဲ"
        If user ask about "Boosting", just say sorry we don't do boosting.
        If you don't find the related answer, just say "တောင်းပန်ပါတယ်။ လက်ရှိမှာ အဲ့မေးခွန်းအတွက် ပြင်ဆင်နေဆဲဖြစ်လို့ Page CB မှာမေးပေးပါနော်။"
        But don't say words like according to provided text.
        Please reply only in BURMESE."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]),
     'Printing': ChatPromptTemplate.from_messages([
        ("system", """
        Your task is to respond to users in a friendly, fun, polite and informative manner.
        You have to provide information about printing design related questions only based on the context: {context}.
        DON'TINVENT OR CHANGE ANY INFORMATION, ESPECIALLY THE PRICING!
        for e.g. "Pamphlet Design တွေက ဘယ်လိုယူလဲ" "Pamphlet ဈေးဘယ်လိုယူလဲ" "Business Card Design ဆွဲပေးလား"
        If you don't find the related answer and is asked about offset printing services, just say "တောင်းပန်ပါတယ်။ လက်ရှိမှာ အဲ့မေးခွန်းအတွက် ပြင်ဆင်နေဆဲဖြစ်လို့ Page CB မှာမေးပေးပါနော်။"
        But don't say words like according to provided text.
        Please reply only in BURMESE."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]),
    'Recommender': ChatPromptTemplate.from_messages([
        ("system", """ You are a friendly, fun, polite, and informative assistant helping users choose the right social media ad package.

            Your job is to guide users toward the most suitable package based on how frequently they plan to post on social media.

            🚫 IMPORTANT: Only recommend from the following three official social ads packages:
            - 4 Photo per month Package
            - 8 Photo per month Package
            - 12 Photo per month Package

            Do NOT invent or mention any other packages.
            🎯 When a user asks about which social media ad package they should purchase, start by asking:
            “How many posts do you plan to publish per month?”
            The user answer may be in how many posts per week, you are required to calculate how many posts per month.

            Then, based on their answer, recommend the most appropriate package from the list above.

            Stay focused only on **social ads packages**. Do not mention boosting plans or any unrelated services.

            Be friendly, clear, and helpful!

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
FAQ node handles introductions, small talk, compliments, and general frequently asked questions only.
Typical questions include:
"Swel Pay Lar ဆိုတာ ဘာလဲ"
"ဘယ်လိုဝန်ဆောင်မှုတွေရှိလဲ"
"ပြန်ပြင်တာဘယ်နှခါပေးလဲ"
"ဆက်သွယ်ဖို့ဘယ်မှာတွေရှိလဲ"
"ငွေပေးချေမှုနည်းလမ်းတွေဘာတွေရှိလဲ"
"ဈေးနှုန်းက ဘာတွေလဲ" or "ဘယ်လောက်လဲ"
"Design Sample တွေ ပြပေးလို့ရလား"
"Content ရော ရေးပေးလား"
"Boosting Service တွေရှိလား"
"UI UX Design တွေ ဆွဲပေးလား"

The Logo involves logo related question such as Logo Packages and logo design fees
The SocialAds involves social media (ads) design related question such as Social media Packages and fees
The Printing involves printing related question such as pamphlet or business card design fees.
The Recommender helps users what kind of social ads package they need.
If you can't find anything related to the above topics, then reply not_found
"""

# route_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", system),
#         ("human", "{question}"),
#     ]
# )
# question_router = route_prompt | structured_llm_router

route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system + """
        IMPORTANT: If the user is asking a follow-up question about a previous topic (like pricing after discussing packages), 
        route to the same category as the previous question. Pay special attention to follow-up questions about pricing, sample designs, or details
        that might refer to previously discussed services."""),
        MessagesPlaceholder(variable_name="chat_history"),  # Add chat history here
        ("human", "{question}"),
    ]
)
question_router = route_prompt | structured_llm_router
