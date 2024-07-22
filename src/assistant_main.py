from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import ToolNode, tools_condition

from src.util import State, llm, Assistant, builder
from src.tools import main_tools, ToReminderAssistant, ToMainAssistant


main_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful personal assistant."
            " Your primary role is manage the user's tasks."
            f" The time right now is {datetime.now()}."
            " The date and time format should be: '%Y-%m-%d %H:%M:%S'."
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())

main_assistant_runnable = main_assistant_prompt | llm.bind_tools(
    main_tools +
    [ToReminderAssistant]
)

def route_main_assistant(state: State):
    route = tools_condition(state)
    if route == "__end__":
        return "__end__"
    
    tool_calls = state["messages"][-1].tool_calls
    if tool_calls:
        if tool_calls[0]["name"] == ToReminderAssistant.__name__:
            return "enter_reminder_assistant"
        return "main_tools"

def to_main_assistant(state: State) -> dict:
    tool_calls = state["messages"][-1].tool_calls
    for tc in tool_calls:
        if tc["name"] == ToMainAssistant.__name__:
            to_main_tc_id = tc["id"]

    return {
        "messages": [
            ToolMessage(
                content="Resume dialog with the main assistant. Please reflect on the past conversation and assist the user as needed.",
                tool_call_id=to_main_tc_id
            )
        ]
    }

def create_main_assistant():
    builder.add_node("main_assistant", Assistant(main_assistant_runnable))
    builder.add_node("main_tools", ToolNode(main_tools))
    builder.add_node("to_main_assistant", to_main_assistant)

    builder.set_entry_point("main_assistant")
    builder.add_conditional_edges("main_assistant", route_main_assistant)
    builder.add_edge("main_tools", "main_assistant")
    builder.add_edge("to_main_assistant", "main_assistant")
