from state import GhajiniState
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class GoalExtraction(BaseModel):
    goal:str
    target_date:str="Not set"
    progress:str="Not started"

chat = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))

def load_goals():
    if not os.path.exists("data/goals.json"):
        return [] # return empty list if file doesn't exist
    with open("data/goals.json", "r") as f: # open file in read mode
        return json.load(f) # load existing goals from file
    
def save_goal(goal:dict):
    goals = load_goals() # load existing goals
    goals.append(goal) # add new goal to list
    with open("data/goals.json", "w") as f: # open file in write mode
        json.dump(goals, f, indent=2) # save updated goals list to file

def goal_node(state:GhajiniState)->GhajiniState:
    if "goal" in state['router_decision']:
       structured_chat = chat.with_structured_output(GoalExtraction)
       result = structured_chat.invoke([
           SystemMessage(content="""You are a goal extraction agent. Your job is to extract any long-term ambitions, aspirations, or goals from the user's message. Always respond with a JSON object containing the following fields:
           - goal: The extracted goal description
           - target_date: The target date for achieving the goal (if any)
           - progress: The current progress towards the goal (if any)
           """  ),
           HumanMessage(content=state['message'])
       ])
       save_goal(result.model_dump())
       return {
            "agent_outputs":{
                **state['agent_outputs'],
                "goal": f"Extracted goal: {result.goal}, target date: {result.target_date}, progress: {result.progress}"
            }
     }  
    goals=load_goals()
    return {
        "agent_outputs":{
            **state['agent_outputs'],
            "goal": f"Current goals: {goals}"
        }
    }
