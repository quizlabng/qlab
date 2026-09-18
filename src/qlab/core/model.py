from pydantic import BaseModel

class User(BaseModel):
    id: str
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None

test_user = User(
    id="1575156816",
    first_name="Taofeek",
    last_name="Abdulazeez",
    username="sirfeeky"
)