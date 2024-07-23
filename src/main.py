import uuid
import os
import schedule
import time
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

    def send_reminder():
        events = graph.stream(
            {"messages": ("user", "send reminder of upcoming tasks tomorrow")}, config, stream_mode="values"
        )
        for event in events:
            if "messages" in event:
                event["messages"][-1].pretty_print()
    
    send_reminder()
    # schedule.every(3).seconds.do(send_reminder)

    # start_time = time.time()

    # while time.time() - start_time < 9:
    #     schedule.run_pending()


if __name__ == "__main__":
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "Taskbot"

    main()