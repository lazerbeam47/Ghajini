from state import GhajiniState
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from datetime import datetime
from zoneinfo import ZoneInfo

load_dotenv()

class TaskExtraction(BaseModel):
    task:str
    date:str
    completed:bool=False

chat = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))
TIMEZONE = ZoneInfo(os.getenv("TIMEZONE", "Asia/Kolkata"))
def load_tasks():
    if not os.path.exists("data/tasks.json"):
        return [] # return empty list if file doesn't exist
    with open("data/tasks.json", "r") as f: # open file in read mode
        return json.load(f) # load existing tasks from file

def save_task(task:dict):
    tasks = load_tasks() # load existing tasks
    tasks.append(task) # add new task to list
    with open("data/tasks.json", "w") as f: # open file in write mode
        json.dump(tasks, f, indent=2) # save updated tasks list to file
def task_node(state:GhajiniState)->GhajiniState:
    if "task" in state['router_decision']:
       structured_chat = chat.with_structured_output(TaskExtraction)
       now = datetime.now(TIMEZONE).strftime("%Y-%m-%d %H:%M")
       result = structured_chat.invoke([
           SystemMessage(content="""You are a task extraction agent. Your job is to extract any tasks, deadlines, or time-sensitive actions from the user's message. Always respond with a JSON object containing the following fields:
           - task: The extracted task description
           - date: The due date for the task in exactly YYYY-MM-DD HH:MM format. Infer relative dates and times from the current datetime provided below. If there is no reminder time, return an empty string.
           - completed: Whether the task is completed or not
           """  ),
           HumanMessage(content=f"Current datetime: {now}"),
           HumanMessage(content=state['message'])
       ])
       task = result.model_dump()
       task["user_id"] = state["user_id"]
       save_task(task)
       return {
            "agent_outputs":{
                **state['agent_outputs'],
                "task": f"Extracted task: {result.task}, date: {result.date}, completed: {result.completed}"
            }
     }  
    tasks=load_tasks()
    return {
        "agent_outputs":{
            **state['agent_outputs'],
            "task": f"Pending tasks: {tasks}"
        }
    }  
