from dataclasses import dataclass
from typing import Any

@dataclass
class BaseResponse:
    message: str
    data: Any

    def __init__(self, message="success", data=None):
        self.message = message
        self.data = data

@dataclass
class ChatResponse:
    content: str

    def __init__(self, content: str):
        self.content = content