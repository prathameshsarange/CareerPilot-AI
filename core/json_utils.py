import json


def parse_json_response(text: str) -> dict:
    """Clean and parse a JSON response from Gemini, stripping markdown fences if present."""
    if not text:
        raise ValueError("Empty response received from Gemini.")

    cleaned = text.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned.removeprefix("```json").removesuffix("```").strip()

    elif cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```").removesuffix("```").strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start == -1 or end == -1 or end < start:
        raise ValueError(f"No JSON object found in Gemini response.\n\nRaw response:\n{text}")

    cleaned = cleaned[start:end + 1]

    try:
        return json.loads(cleaned)

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON received from Gemini.\n\n{e}\n\nRaw response:\n{text}") from e
