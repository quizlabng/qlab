from pydantic import BaseModel
from qlab.core.model import User


class ChatRequest(BaseModel):
    message: str
    user: User