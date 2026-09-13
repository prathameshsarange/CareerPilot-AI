from google.genai import types

from core.gemini_client import get_gemini_client
from core.prompts import CAREER_ADVISOR_PROMPT
from core.json_utils import parse_json_response
from schemas.report_schema import CareerAdvisorResponse


class CareerAdvisorAgent:

    def advise(self, career_domain: dict, skill_gap: dict) -> dict:

        prompt = f"""
{CAREER_ADVISOR_PROMPT}

Career Domain:

{career_domain}

Skill Gap:

{skill_gap}
"""

        response = get_gemini_client().models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=CareerAdvisorResponse,
            ),
        )

        if response.parsed is not None:
            return response.parsed.model_dump()

        return parse_json_response(response.text)
