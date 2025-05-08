from pydantic import BaseModel
from typing import Literal

class BaseMessage(BaseModel):
    content: str
    role: str

class SystemMessage(BaseMessage):
    role: Literal["system"] = "system"

class HumanMessage(BaseMessage):
    role: Literal["human"] = "human"

class AIMessage(BaseMessage):
    role: Literal["ai"] = "ai" 