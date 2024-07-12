from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import ToolNode, tools_condition

from src.util import State, builder, llm, Assistant, create_entry_node
from src.tools import delete_tasks_tools, ToMainAssistant

delete_tasks_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a specialized assistant for deleting tasks."
            "First, retrieve all the tasks from the database."
            "Then, compare the user's query with all the tasks the user has, decide which task the user wants to delete."
            "Finally, delete the task from the database."
            "After the action is complete, go back to the main assistant."
            "If the user's query doesn't match any task in the database, say the task doesn't exist and don't delete anything."
            # "Only call the most appropriate tool one at a time."
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())

delete_tasks_assisant_runnable = delete_tasks_assistant_prompt | llm.bind_tools(
    delete_tasks_tools + [ToMainAssistant]
)

def route_delete_tasks(state: State):
    route = tools_condition(state)
    if route == "__end__":
        return "__end__"
    
    tool_calls = state["messages"][-1].tool_calls
    action_complete = any(tc["name"] == ToMainAssistant.__name__ for tc in tool_calls)
    if action_complete:
        return "to_main_assistant"
    return "delete_tasks_tools"


def create_assistant_delete():
    builder.add_node("enter_delete_tasks", create_entry_node("delete task assistant"))
    builder.add_node("delete_tasks_assistant", Assistant(delete_tasks_assisant_runnable))
    builder.add_node("delete_tasks_tools", ToolNode(delete_tasks_tools))

    builder.add_edge("enter_delete_tasks", "delete_tasks_assistant")
    builder.add_conditional_edges("delete_tasks_assistant", route_delete_tasks)
    builder.add_edge("delete_tasks_tools", "delete_tasks_assistant")