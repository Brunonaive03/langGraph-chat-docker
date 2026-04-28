from typing import Annotated, TypedDict, List, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class PokedexState(TypedDict):
    # add_messages ensures new messages are appended rather than overwriting
    messages: Annotated[List[BaseMessage], add_messages]