from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    theme: str = Field(min_length=2)
    platform: str = Field(min_length=2)
    region: str = "global"
    budget_mode: str = "balanced"
    task_type: str = "creative"


class GenerateResponse(BaseModel):
    idea: str
    audience: str
    monetization: str
    risks: list[str]
    sources: list[str]
    provider: str
    model: str
    profile: str


class ErrorResponse(BaseModel):
    code: str
    message: str
