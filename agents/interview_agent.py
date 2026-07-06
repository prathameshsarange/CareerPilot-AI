from core.gemini_client import get_gemini_client
from core.prompts import INTERVIEW_PROMPT
from core.json_utils import parse_json_response


class InterviewAgent:

    def generate(self, resume_analysis: dict) -> dict:

        prompt = f"""
{INTERVIEW_PROMPT}

Resume Agent Output:

{resume_analysis}
"""

        response = get_gemini_client().models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return parse_json_response(response.text)
