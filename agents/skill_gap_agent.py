from core.gemini_client import get_gemini_client
from core.prompts import SKILL_GAP_PROMPT
from core.json_utils import parse_json_response


class SkillGapAgent:

    def analyze(self, resume_analysis: dict) -> dict:

        prompt = f"""
{SKILL_GAP_PROMPT}

Resume Agent Output:

{resume_analysis}
"""

        response = get_gemini_client().models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return parse_json_response(response.text)
