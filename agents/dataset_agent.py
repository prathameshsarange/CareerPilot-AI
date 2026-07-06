import pandas as pd

from core.gemini_client import get_gemini_client


class DatasetAgent:

    def analyze(self, file_path):

        df = pd.read_csv(file_path)

        prompt = f"""
You are a Senior Data Scientist.

Analyze this dataset.

Columns:
{list(df.columns)}

Shape:
{df.shape}

Missing Values:
{df.isnull().sum().to_string()}

Summary:
{df.describe(include='all').to_string()}

Give:

# Dataset Overview

# Data Quality Issues

# Business Insights

# Interesting Patterns

# Recommendations
"""

        response = get_gemini_client().models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text
