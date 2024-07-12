

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Literal, Callable
from taskbot.src.util import State
from taskbot.src.assistant_main import Assistant, main_assistant_runnable, delete_tasks_assisant_runnable, BackToMainAssistant
from taskbot.src.tools import main_tools, delete_tasks_tools, ToDeleteTasks, get_all_tasks

# def get_all_tasks(state: State):
    # get all tasks
    # let llm decide which one user is deleting
    # returning task_id to delete
    # delete task from db



