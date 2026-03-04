from langgraph.graph import StateGraph, END

from graph.state import AgentState
from graph.nodes import (
    intent_extraction_node,
    country_api_node,
    answer_synthesis_node
)

def build_agent():

    workflow = StateGraph(AgentState)

    # Register nodes
    workflow.add_node("intent", intent_extraction_node)
    workflow.add_node("country_api", country_api_node)
    workflow.add_node("answer", answer_synthesis_node)

    # Define flow
    workflow.set_entry_point("intent")

    workflow.add_edge("intent", "country_api")
    workflow.add_edge("country_api", "answer")
    workflow.add_edge("answer", END)

    return workflow.compile()