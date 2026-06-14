from langgraph.graph import StateGraph, END, START
from state import GhajiniState
from agents.memory import memory_node
from agents.router import router_node
from agents.response import response_node   
from agents.task import task_node
from agents.coach import coach_node
from agents.goal import goal_node


graph = StateGraph(GhajiniState)

#add nodes
graph.add_node("router", router_node)
graph.add_node("memory", memory_node)
graph.add_node("task", task_node)
graph.add_node("goal", goal_node)
graph.add_node("coach", coach_node)
graph.add_node("response", response_node)

#add edges
graph.add_edge(START, "router")
graph.add_edge("router", "memory")
graph.add_edge("memory", "task")
graph.add_edge("task", "goal")
graph.add_edge("goal", "coach")
graph.add_edge("coach", "response")
graph.add_edge("response", END)

app=graph.compile()

