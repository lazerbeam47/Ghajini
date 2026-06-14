from state import GhajiniState
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
import os
from dotenv import load_dotenv


load_dotenv()

chat = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))

def coach_node(state:GhajiniState)->GhajiniState:
    if "coach" in state['router_decision']:
        result = chat.invoke([
            SystemMessage(content="""You are a helpful, motivating, well informed and empathetic coach agent. Your job is to provide advice, guidance, and support to the user based on their current situation and goals.
            """  ),
            HumanMessage(content=f"""
                         User message: {state['message']}
                         Retrieved memories: {state['retrieved_memories']}
                         Pending tasks: {state['agent_outputs'].get('task', 'No tasks')}
                         Current goals: {state['agent_outputs'].get('goal', 'No goals')}
                         """),
        ])
        return {
            "agent_outputs": {
                **state['agent_outputs'],
                "coach": result.content
            }
        }
    return {
        "agent_outputs": {
            **state['agent_outputs'],
            "coach": "No coaching advice since coach agent was not activated."
        }
    }