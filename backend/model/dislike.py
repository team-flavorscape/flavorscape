from pydantic import BaseModel

class Dislike(BaseModel):
    id: int
    name: str

