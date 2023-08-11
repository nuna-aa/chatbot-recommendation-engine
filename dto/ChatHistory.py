from typing import List, Any

from pydantic import BaseModel


class ChatHistory(BaseModel):
    history: List[Any]
