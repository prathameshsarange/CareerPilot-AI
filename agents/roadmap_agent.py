from core.gemini_client import get_gemini_client
from core.prompts import ROADMAP_PROMPT
from core.json_utils import parse_json_response


class RoadmapAgent:

    def generate(self, skill_gap: dict) -> dict:

        prompt = f"""
{ROADMAP_PROMPT}

Skill Gap Agent Output:

{skill_gap}
"""

        response = get_gemini_client().models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return parse_json_response(response.text)
