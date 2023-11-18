from pydantic import BaseModel

class Recipe(BaseModel):
    id: int
    name: str
    img_url: str
    ingredients: list[str]
    allergens: list[str]

