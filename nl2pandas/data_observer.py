from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass
class DataMetadata:
    filename: str
    shape: tuple[int, int]
    columns: list[str]
    dtypes: dict[str, str]
    sample_rows: list[dict[str, Any]]


class DataObserver:
    @staticmethod
    def load_excel(uploaded_file) -> pd.DataFrame:
        return pd.read_excel(uploaded_file)

    @staticmethod
    def build_metadata(df: pd.DataFrame, filename: str) -> DataMetadata:
        sample_df = df.head(3)
        return DataMetadata(
            filename=filename,
            shape=df.shape,
            columns=df.columns.tolist(),
            dtypes={column: str(dtype) for column, dtype in df.dtypes.to_dict().items()},
            sample_rows=sample_df.to_dict(orient="records"),
        )