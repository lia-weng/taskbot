from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from src.state import State
from dotenv import load_dotenv
from langchain_core.pydantic_v1 import BaseModel
from src.assistant_tools import main_tools, ToDeleteTasks, delete_tasks_tools

load_dotenv()

class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            result = self.runnable.invoke(state)
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")


main_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful personal assistant."
            "Your primary role is manage the user's tasks."
            f"The time right now is {datetime.now()}."
            "Use this information to process the user's queries."
            "Only call the most appropriate tool one at a time."
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())

main_assistant_runnable = main_assistant_prompt | llm.bind_tools(
    main_tools +
    [ToDeleteTasks]
)

class BackToMainAssistant(BaseModel):
    """A tool for routing back to the main assistant."""


delete_tasks_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a specialized assistant for deleting tasks."
            "First, retrieve all the tasks from the database."
            "Then, compare the user's query with all the tasks the user has, decide which task the user wants to delete."
            "Finally, delete the task from the database."
            "Once deletion is complete, go back to the main assistant."
            "Only call one tool at a time."
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())

delete_tasks_assisant_runnable = delete_tasks_assistant_prompt | llm.bind_tools(
    delete_tasks_tools + [BackToMainAssistant]
)