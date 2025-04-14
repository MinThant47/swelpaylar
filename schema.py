from typing_extensions import TypedDict
from langgraph.graph import START, END, StateGraph
from node_func import State, inquiry, FAQ, Recommender, Logo, SocialAds, Printing, not_found, route_app

workflow = StateGraph(State)

workflow.add_node("inquiry", inquiry)
workflow.add_node("FAQ", FAQ)
workflow.add_node("Logo", Logo)
workflow.add_node("SocialAds", SocialAds)
workflow.add_node("Printing", Printing)
workflow.add_node("Recommender", Recommender)
workflow.add_node("not_found", not_found)

workflow.add_edge(START, "inquiry")
workflow.add_conditional_edges("inquiry", route_app)
workflow.add_edge("FAQ", END)
workflow.add_edge("Logo", END)
workflow.add_edge("SocialAds", END)
workflow.add_edge("Printing", END)
workflow.add_edge("Recommender", END)
workflow.add_edge("not_found", END)

app = workflow.compile()