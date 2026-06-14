from state import GhajiniState
from memory.store import store_memory, retrieve_memory

def memory_node(state:GhajiniState) -> dict:
    if "memory" in state['router_decision']:
        store_memory(state['message'], state['user_id'])

    retrieved = retrieve_memory(state['message'], state['user_id'])
    
    return {
        "retrieved_memories": retrieved,
        "agent_outputs":{
            **state['agent_outputs'],
            "memory": f"Stored message: {state['message']}\nRetrieved memories: {retrieved}"
        }
    }
