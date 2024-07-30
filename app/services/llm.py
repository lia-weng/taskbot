import uuid
from langchain_core.messages import HumanMessage

from assistant.graph import create_graph

graph = create_graph()
thread_id = str(uuid.uuid4())

config = {
    "configurable": {
        "thread_id": thread_id,
    }
}

def invoke_llm(user_message: str):
    result = graph.invoke(
            {
                "messages": [
                    HumanMessage(content=user_message)
                ]
            },
            config
        )
    
    return result["messages"][-1].content