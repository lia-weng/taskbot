import uuid
import os
from dotenv import load_dotenv
from src.graph import create_graph


def main():
    graph = create_graph()
    thread_id = str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    questions = [
        # "add task do laundry for Saturday",
        # "add meet with friends for July 15 at 8pm",
        # "add call bank for july 20",
        # "finish essay for next wednesday"
        # "Which tasks have I not started yet?",
        # "What do I have left in July?",
        # "What's my task for this week"
        # "What's my tasks between 7/15 to end of the month?",
        # "Add go to work social for this Sunday",
        "I want to delete the task: essay"
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
