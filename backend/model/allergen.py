from pydantic import BaseModel

class Allergen(BaseModel):
    id: int
    name: str

