from core.gemini_client import get_gemini_client
from core.prompts import CAREER_ADVISOR_PROMPT
from core.json_utils import parse_json_response


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
            contents=prompt
        )

        return parse_json_response(response.text)
