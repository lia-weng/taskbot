import uuid
import os
import schedule
import time
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
# import subprocess

from data.csv_to_sql import populate_data
from src.util import builder
from src.assistant_main import create_main_assistant
from src.assistant_reminder import create_reminder_assistant


def main():
    # populate_data()
    create_main_assistant()
    create_reminder_assistant()

    memory = SqliteSaver.from_conn_string(":memory:")
    graph = builder.compile(checkpointer=memory)
    thread_id = str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    def send_reminder():
        print(time.time())
        events = graph.stream(
            {"messages": ("user", "send reminder of upcoming tasks within next 3 days")}, config, stream_mode="values"
        )
        for event in events:
            if "messages" in event:
                event["messages"][-1].pretty_print()
    
    schedule.every(3).seconds.do(send_reminder)

    start_time = time.time()

    while time.time() - start_time < 9:
        schedule.run_pending()

# def main():
#     populate_data()
#     create_main_assistant()
#     create_reminder_assistant()

#     memory = SqliteSaver.from_conn_string(":memory:")
#     graph = builder.compile(checkpointer=memory)
#     thread_id = str(uuid.uuid4())

#     config = {
#         "configurable": {
#             "thread_id": thread_id,
#         }
#     }

#     questions = [
#         # "add task do laundry for Saturday",
#         # "add meet with friends for July 15 at 8pm",
#         # "Which tasks have I not started yet?",
#         # "What do I have left in September?",
#         # "What's my task for this week",
#         # "What's my tasks between 7/15 to end of the month?",
#         "send me a reminder of tasks",
#         # "I want to delete the task: call the bank",

#     ]

#     for question in questions:
#         events = graph.stream(
#             {"messages": ("user", question)}, config, stream_mode="values"
#         )
#         for event in events:
#             if "messages" in event:
#                 event["messages"][-1].pretty_print()


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