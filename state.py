from typing import TypedDict, List ,Dict

class GhajiniState(TypedDict):
    message: str
    user_id: str
    router_decision: List[str]
    retrieved_memories: List[str]
    agent_outputs: Dict[str, str]
    final_response: str