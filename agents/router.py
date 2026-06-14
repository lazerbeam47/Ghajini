from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from state import GhajiniState
from pydantic import BaseModel
from typing import List
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY)

class RouterDecision(BaseModel):
    agents: List[str]

def router_node(state: GhajiniState) -> dict:
    # hard rule first
    if state['message'].startswith("*"):
        return {"router_decision": ["memory", "response"]}
    
    # LLM decides everything else
    current_messages = [
        SystemMessage(content="""You are a router agent in a multi-agent system. Your task is to analyze the user's message and decide which agents should handle the request. The available agents are:
            memory  → activate when message contains personal facts,
                    preferences, or information about the user
            task    → activate when message contains a deadline,
                    todo, or time-sensitive action
            goal    → activate when message contains long term
                    ambitions or aspirations
            coach   → activate when user is asking for advice,
                    guidance, or what to do next
            response → ALWAYS activate, every single message
        """),
        HumanMessage(content=state['message'])
    ]
    structured_chat = chat_model.with_structured_output(RouterDecision)
    result = structured_chat.invoke(current_messages)
    return {"router_decision": result.agents}

