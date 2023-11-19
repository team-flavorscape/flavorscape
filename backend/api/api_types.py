from pydantic import BaseModel

class OnboardCheckResponse(BaseModel):
    isOnboarded: bool

class OnboardRequest(BaseModel):
    allergens: list[int] | None = []
    dislikes: list[int] | None = []

class RatingRequest(BaseModel):
    recipe_id: int
    rating: int

class ResultResponse(BaseModel):
    success: bool

class WeeklyPlanRequest(BaseModel):
    recipe_id: int
