from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    theme: str = Field(min_length=2, max_length=500, description="Theme or niche for idea generation")
    platform: str = Field(min_length=2, max_length=100, description="Target platform (tiktok, mobile, etc)")
    region: str = Field(default="global", max_length=50, description="Target region")
    budget_mode: str = Field(default="balanced", pattern=r"^(balanced|low_cost)$", description="balanced|low_cost")
    task_type: str = Field(
        default="creative", pattern=r"^(creative|analysis|reasoning)$", description="creative|analysis|reasoning"
    )


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
