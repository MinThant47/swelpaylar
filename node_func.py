from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage, BaseMessage
from llm_and_route_query import llm, question_router, prompt
from typing_extensions import TypedDict, List
from load import get_context

class State(TypedDict):
  question: str
  topic: str
  response: str
  chat_history: List[BaseMessage]

def inquiry(state: State) -> State:
    question = state["question"]
    source = question_router.invoke({"question": question, "chat_history":state["chat_history"]})
    if source.datasource == "FAQ":
        print("---ROUTE QUESTION TO FAQ---")
        return {"topic" : "FAQ"}
    elif source.datasource == "SocialAds":
        print("---ROUTE QUESTION TO SocialAds---")
        return {"topic" : "SocialAds"}
    elif source.datasource == "Logo":
        print("---ROUTE QUESTION TO Logo---")
        return {"topic" : "Logo"}
    elif source.datasource == "Printing":
        print("---ROUTE QUESTION TO Printing---")
        return {"topic" : "Printing"}
    elif source.datasource == "Recommender":
        print("---ROUTE QUESTION TO Recommender---")
        return {"topic" : "Recommender"}
    else:
        print("Can't find related documents")
        return {"topic" : "not_found"}


def FAQ(state: State) -> State:
  print("Routing to FAQ : ")
  question = state["question"]
  response = get_context("SPLFAQ", question, prompt['FAQ'], state["chat_history"])
  return {"response": response}


def Logo(state: State) -> State:
  print("Routing to Logo : ")
  question = state["question"]
  response = get_context("SPLLogo", question, prompt['Logo'], state["chat_history"])
  return {"response": response}


def SocialAds(state: State) -> State:
  print("Routing to SocialAds : ")
  question = state["question"]
  response = get_context("SPLSocialAds", question, prompt['SocialAds'], state["chat_history"])
  return {"response": response}

  
def Printing(state: State) -> State:
  print("Routing to Printing : ")
  question = state["question"]
  response = get_context("SPLPrinting", question, prompt['Printing'], state["chat_history"])
  return {"response": response}


def Recommender(state: State) -> State:
  print("Routing to Recommender : ")
  question = state["question"]
  llm_recommender = prompt['Recommender'] | llm
  raw_answer = llm_recommender.invoke({"input": question, "chat_history": state["chat_history"]})

  response = {"answer": raw_answer.content}
  return {"response": response}

def not_found(state: State) -> State:
  print("Not Found: Out of scope")

  question = HumanMessage(content=state["question"] + "The answer to the question isn't available in the document.")
  system_message = SystemMessage(content="You provides polite and concise reponse when there is no relevant information, please check Page CB in burmese.")

  response = {"input": question, "answer": llm.invoke([system_message, question]).content}

  return {"response": response}


def route_app(state: State) -> str:
  if(state["topic"] == "FAQ"):
    return "FAQ"
  elif(state["topic"] == "Logo"):
    return "Logo"
  elif(state["topic"] == "SocialAds"):
    return "SocialAds"
  elif(state["topic"] == "Printing"):
    return "Printing"
  elif(state["topic"] == "Recommender"):
    return "Recommender"
  elif(state["topic"] == "not_found"):
    return "not_found"
