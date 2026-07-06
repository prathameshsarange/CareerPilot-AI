from core.gemini_client import get_gemini_client
from core.prompts import RESUME_SYSTEM_PROMPT
from core.json_utils import parse_json_response


class ResumeAgent:

    def analyze_resume(self, resume_text: str) -> dict:

        prompt = f"""
{RESUME_SYSTEM_PROMPT}

Resume:

{resume_text}
"""

        response = get_gemini_client().models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return parse_json_response(response.text)
