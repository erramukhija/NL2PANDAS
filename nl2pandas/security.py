from __future__ import annotations

import threading
from typing import Any

import pandas as pd


def strip_markdown(code: str) -> str:
    cleaned_code = code.strip()
    if cleaned_code.startswith("```"):
        cleaned_code = cleaned_code.split("\n", 1)[-1]
    if cleaned_code.endswith("```"):
        cleaned_code = cleaned_code.rsplit("```", 1)[0]
    return cleaned_code.strip()


def contains_forbidden_keywords(code: str, forbidden_keywords: list[str]) -> bool:
    lower_code = code.lower()
    return any(keyword.lower() in lower_code for keyword in forbidden_keywords)


def run_with_timeout(code: str, local_vars: dict[str, Any], timeout_seconds: int = 10) -> None:
    exception_holder: list[Exception | None] = [None]

    def target() -> None:
        try:
            exec(code, {"__builtins__": {}}, local_vars)
        except Exception as execution_error:
            exception_holder[0] = execution_error

    execution_thread = threading.Thread(target=target, daemon=True)
    execution_thread.start()
    execution_thread.join(timeout=timeout_seconds)

    if execution_thread.is_alive():
        raise TimeoutError(
            f"Execution exceeded {timeout_seconds} second limit. Try a more specific query."
        )
    if exception_holder[0] is not None:
        raise exception_holder[0]


def execute_generated_code(code: str, source_df: pd.DataFrame, timeout_seconds: int) -> Any:
    local_vars: dict[str, Any] = {"df": source_df.copy(), "pd": pd}
    run_with_timeout(code=code, local_vars=local_vars, timeout_seconds=timeout_seconds)

    if "ans" not in local_vars:
        raise ValueError("Model did not assign a result to 'ans'. Try rephrasing your query.")

    result = local_vars.get("ans")
    if result is None:
        raise ValueError("Model did not assign a result to 'ans'. Try rephrasing your query.")

    return result