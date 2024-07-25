from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph

from data.csv_to_sql import populate_data
from assistant.assistant_main import create_main_assistant
from assistant.assistant_reminder import create_reminder_assistant
from assistant.util import builder


def create_graph():
    create_main_assistant()
    create_reminder_assistant()

    memory = SqliteSaver.from_conn_string(":memory:")
    graph = builder.compile(checkpointer=memory)
    return graph

