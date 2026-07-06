from core.gemini_client import get_gemini_client


class MLAdvisorAgent:

    def suggest(self, dataset_analysis):

        prompt = f"""
Based on this dataset analysis:

{dataset_analysis}

Suggest:

1. Problem Type
2. Best ML Algorithm
3. Why
4. Evaluation Metrics
5. Feature Engineering Ideas
"""

        response = get_gemini_client().models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text
