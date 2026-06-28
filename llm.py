from __future__ import annotations

import google.generativeai as genai

from nl2pandas.data_observer import DataMetadata


def build_system_prompt(metadata: DataMetadata, query: str) -> str:
    dtypes_text = metadata.dtypes
    shape_text = metadata.shape
    sample_text = metadata.sample_rows

    return f"""
You are a data retrieval expert. You are given a DataFrame 'df' with the following schema:
- Columns & types: {dtypes_text}
- Shape: {shape_text}
- Sample (3 rows): {sample_text}

Rules:
1. Write ONLY raw Python (Pandas) code. No explanations, no markdown, no comments.
2. Assign the final result to a variable named 'ans'.
3. Do not import any libraries.
4. Do not modify the original 'df'. Use df.copy() if transformation is needed.
5. Unless the user explicitly asks for specific columns or rows, return the full DataFrame shape (all columns).
6. If the query is not about data retrieval or analysis, return exactly: SECURITY_ISSUE

Query: {query}
""".strip()


def generate_code_with_gemini(
    api_key: str,
    model_name: str,
    metadata: DataMetadata,
    query: str,
) -> str:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    prompt = build_system_prompt(metadata=metadata, query=query)
    response = model.generate_content(prompt)

    if not response or not getattr(response, "text", None):
        raise ValueError("Model returned an empty response.")

    return response.text.strip()