from google.genai import types

from core.gemini_client import get_gemini_client
from core.prompts import SKILL_GAP_PROMPT
from core.json_utils import parse_json_response
from schemas.report_schema import SkillGapResponse


class SkillGapAgent:

    def analyze(self, resume_analysis: dict) -> dict:

        prompt = f"""
{SKILL_GAP_PROMPT}

Resume Agent Output:

{resume_analysis}
"""

        response = get_gemini_client().models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=SkillGapResponse,
            ),
        )

        if response.parsed is not None:
            return response.parsed.model_dump()

        return parse_json_response(response.text)
