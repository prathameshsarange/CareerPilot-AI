from google.genai import types

from core.gemini_client import get_gemini_client
from core.prompts import INTERVIEW_PROMPT
from core.json_utils import parse_json_response
from schemas.report_schema import InterviewResponse


class InterviewAgent:

    def generate(self, resume_analysis: dict) -> dict:

        prompt = f"""
{INTERVIEW_PROMPT}

Resume Agent Output:

{resume_analysis}
"""

        response = get_gemini_client().models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=InterviewResponse,
            ),
        )

        if response.parsed is not None:
            return response.parsed.model_dump()

        return parse_json_response(response.text)
