from langgraph.checkpoint.sqlite import SqliteSaver

from assistant.assistant_main import create_main_assistant
from assistant.util import builder


def create_graph():
    create_main_assistant()

    memory = SqliteSaver.from_conn_string(":memory:")
    graph = builder.compile(checkpointer=memory)
    return graph

