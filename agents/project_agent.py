from google.genai import types

from core.gemini_client import get_gemini_client
from core.prompts import CAREER_ADVISOR_PROMPT
from core.json_utils import parse_json_response
from schemas.report_schema import CareerAdvisorResponse
from services.salary_service import lookup_salary


class CareerAdvisorAgent:

    def advise(self, career_domain: dict, skill_gap: dict) -> dict:

        prompt = f"""
{CAREER_ADVISOR_PROMPT}

Career Domain:

{career_domain}

Skill Gap:

{skill_gap}
"""

        salary_tool = types.FunctionDeclaration(
            name="lookup_salary",
            description="Look up current salary ranges from live job listings. Use this before giving salary guidance.",
            parameters={
                "type": "object",
                "properties": {
                    "role": {"type": "string", "description": "The target job role."},
                    "location": {"type": "string", "description": "Country or location, such as us or New York."},
                },
                "required": ["role"],
            },
        )
        tool_config = types.GenerateContentConfig(
            tools=[types.Tool(function_declarations=[salary_tool])],
        )
        client = get_gemini_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=tool_config,
        )

        function_calls = response.function_calls or []
        if function_calls:
            function_call = function_calls[0]
            if function_call.name != "lookup_salary":
                raise ValueError(f"Unsupported career advisor tool: {function_call.name}")

            tool_result = lookup_salary(**(function_call.args or {}))
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    prompt,
                    response.candidates[0].content,
                    types.Content(
                        role="tool",
                        parts=[types.Part.from_function_response(
                            name=function_call.name,
                            response={"result": tool_result},
                        )],
                    ),
                ],
                config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=CareerAdvisorResponse,
                ),
            )

        if response.parsed is not None:
            return response.parsed.model_dump()

        return parse_json_response(response.text)
