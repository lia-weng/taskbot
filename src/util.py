from dotenv import load_dotenv
from typing import Annotated, Callable
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.messages import ToolMessage


load_dotenv()

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

llm = ChatOpenAI(
    model="gpt-3.5-turbo-0125",
)

builder = StateGraph(State)

class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            result = self.runnable.invoke(state)
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}

def create_entry_node(assistant_name: str) -> Callable:
    def entry_node(state: State) -> dict:
        tool_call_id = state["messages"][-1].tool_calls[0]["id"]
        return {
            "messages": [
                ToolMessage(
                    content=f"The assistant is now the {assistant_name}. Reflect on the above conversation between the main assistant and the user."
                    " Do not mention who you are. Act only as the proxy assistant.",
                    tool_call_id=tool_call_id,
                )
            ]
        }
    
    return entry_node

# def create_graph():
#     builder = StateGraph(State)

#     # main assistant
#     builder.add_node("main_assistant", Assistant(main_assistant_runnable))
#     builder.add_node("tools", ToolNode(main_tools))
#     builder.add_node("back_to_main_assistant", back_to_main_assistant)

#     builder.set_entry_point("main_assistant")
#     builder.add_conditional_edges("main_assistant", route_tasks)
#     builder.add_edge("tools", "main_assistant")
#     builder.add_edge("back_to_main_assistant", "main_assistant")

#     # delete tasks assistant
#     builder.add_node("enter_delete_tasks", create_entry_node("delete task assistant"))
#     builder.add_node("delete_tasks_assistant", Assistant(delete_tasks_assisant_runnable))
#     builder.add_node("delete_tasks_tools", ToolNode(delete_tasks_tools))

#     builder.add_edge("enter_delete_tasks", "delete_tasks_assistant")
#     builder.add_conditional_edges("delete_tasks_assistant", route_delete_tasks)
#     builder.add_edge("delete_tasks_tools", "delete_tasks_assistant")

#     # The checkpointer lets the graph persist its state
#     memory = SqliteSaver.from_conn_string(":memory:")
#     return builder.compile(checkpointer=memory)
