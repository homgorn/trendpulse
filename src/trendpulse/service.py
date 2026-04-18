import json
import re
from typing import Any

from trendpulse.core.llm.gateway import LLMGateway
from trendpulse.errors import ProviderError
from trendpulse.schemas import GenerateRequest, GenerateResponse

PROMPT_TEMPLATE = """You are TrendPulse idea generator.
Return ONLY strict JSON object with keys:
idea, audience, monetization, risks, sources.
Context:
- theme: {theme}
- platform: {platform}
- region: {region}
"""


class TrendPulseService:
    def __init__(self, gateway: LLMGateway):
        self.gateway = gateway

    async def generate(self, req: GenerateRequest, trace_id: str | None = None) -> GenerateResponse:
        prompt = PROMPT_TEMPLATE.format(
            theme=req.theme,
            platform=req.platform,
            region=req.region,
        )
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": "You produce marketable startup ideas."},
            {"role": "user", "content": prompt},
        ]
        result = await self.gateway.chat(
            messages=messages,
            task_type=req.task_type,
            budget_mode=req.budget_mode,
            region=req.region,
            trace_id=trace_id,
        )
        data = self._parse_json(result.text)
        return GenerateResponse(
            idea=data.get("idea", ""),
            audience=data.get("audience", ""),
            monetization=data.get("monetization", ""),
            risks=list(data.get("risks", [])),
            sources=list(data.get("sources", [])),
            provider=result.provider,
            model=result.model,
            profile=result.profile,
        )

    @staticmethod
    def _parse_json(text: str) -> dict[str, Any]:
        text = text.strip()

        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```\s*$", "", text)
        text = text.strip()

        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            text = text[start : end + 1]

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise ProviderError(f"LLM returned invalid JSON: {e}") from e
