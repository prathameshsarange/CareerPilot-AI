from google.genai import types

from core.gemini_client import get_gemini_client
from core.prompts import RESUME_SYSTEM_PROMPT
from core.json_utils import parse_json_response
from schemas.report_schema import ResumeAgentResponse


class ResumeAgent:

    def analyze_resume(self, resume_text: str) -> dict:

        prompt = f"""
{RESUME_SYSTEM_PROMPT}

Resume:

{resume_text}
"""

        response = get_gemini_client().models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ResumeAgentResponse,
            ),
        )

        # response.parsed is a ResumeAgentResponse instance when structured
        # output succeeds. Fall back to the old free-text parser only if the
        # SDK couldn't populate it (defensive — shouldn't normally trigger).
        if response.parsed is not None:
            return response.parsed.model_dump()

        return parse_json_response(response.text)
