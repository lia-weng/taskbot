from typing import Annotated, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages


# Define the State schema
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
