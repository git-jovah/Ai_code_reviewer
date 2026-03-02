from pydantic import BaseModel, Field
from typing import List

class ReviewRequest(BaseModel):
    code: str = Field(..., min_length=5)
    language: str = Field(..., example="python")

class ReviewResponse(BaseModel):
    security_issues: List[str]
    performance_issues: List[str]
    readability_issues: List[str]
    overall_score: int