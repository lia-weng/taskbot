import uuid
import os
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
import subprocess

from src.util import builder
from src.assistant_main import create_assistant_main
from src.assistant_delete import create_assistant_delete
from data import csv_to_sql


def main():
    subprocess.run(['python', 'data/csv_to_sql.py'])

    create_assistant_main()
    create_assistant_delete()

    memory = SqliteSaver.from_conn_string(":memory:")
    graph = builder.compile(checkpointer=memory)
    thread_id = str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    questions = [
        # "add task do laundry for Saturday",
        # "add meet with friends for July 15 at 8pm",
        # "Which tasks have I not started yet?",
        # "What do I have left in September?",
        # "What's my task for this week"
        # "What's my tasks between 7/15 to end of the month?",
        "I want to delete the task: finish essay"
    ]

    for question in questions:
        events = graph.stream(
            {"messages": ("user", question)}, config, stream_mode="values"
        )
        for event in events:
            if "messages" in event:
                event["messages"][-1].pretty_print()


if __name__ == "__main__":
    load_dotenv()
    # Now you can access the environment variables directly
    openai_api_key = os.getenv("OPENAI_API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "Taskbot"
    # Set other environment variables as needed
    main()
