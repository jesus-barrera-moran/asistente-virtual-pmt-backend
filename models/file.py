from pydantic import BaseModel

class File(BaseModel):
    name: str
    content: str | None = None
