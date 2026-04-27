from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # add_messages ensures new messages are appended to history rather than overwriting
    messages: Annotated[list[BaseMessage], add_messages]