import pandas as pd
import streamlit as st

from nl2pandas.config import (
    APP_TITLE,
    FORBIDDEN_KEYWORDS,
    GEMINI_MODEL,
    RESULT_PREVIEW_ROWS,
    TIMEOUT_SECONDS,
    get_gemini_api_key,
)
from nl2pandas.data_observer import DataObserver
from nl2pandas.exporters import to_excel_bytes
from nl2pandas.llm import generate_code_with_gemini
from nl2pandas.security import contains_forbidden_keywords, execute_generated_code, strip_markdown


def initialize_session_state() -> None:
    defaults = {
        "source_df": None,
        "metadata": None,
        "result": None,
        "raw_llm_response": "",
        "cleaned_code": "",
        "execution_error": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_sidebar_panel() -> None:
    st.subheader("Data Source")
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

    if uploaded_file is None:
        return

    try:
        loaded_df = DataObserver.load_excel(uploaded_file)
        metadata = DataObserver.build_metadata(loaded_df, uploaded_file.name)
        st.session_state.source_df = loaded_df
        st.session_state.metadata = metadata
        st.success("Excel file loaded successfully.")
    except Exception as parse_error:
        st.session_state.source_df = None
        st.session_state.metadata = None
        st.error(f"Could not parse file '{uploaded_file.name}': {parse_error}")
        return

    st.caption("Metadata")
    st.write(f"**Filename:** {st.session_state.metadata.filename}")
    st.write(f"**Shape:** {st.session_state.metadata.shape}")
    st.write("**Columns:**")
    st.code(", ".join(st.session_state.metadata.columns), language="text")


def render_result(result) -> None:
    st.subheader("Result")
    if isinstance(result, pd.DataFrame):
        st.write(f"Rows: {len(result)}")
        st.dataframe(result.head(RESULT_PREVIEW_ROWS), use_container_width=True)
        st.download_button(
            label="Download as Excel",
            data=to_excel_bytes(result),
            file_name="result.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        return

    st.write(result)


def process_query(query: str) -> None:
    st.session_state.execution_error = ""
    st.session_state.raw_llm_response = ""
    st.session_state.cleaned_code = ""
    st.session_state.result = None

    if st.session_state.source_df is None:
        st.warning("Upload an Excel file first.")
        return

    api_key = get_gemini_api_key()
    if not api_key:
        st.error("Set GEMINI_API_KEY in your environment before running queries.")
        return

    try:
        raw_response = generate_code_with_gemini(
            api_key=api_key,
            model_name=GEMINI_MODEL,
            metadata=st.session_state.metadata,
            query=query,
        )
        st.session_state.raw_llm_response = raw_response

        if raw_response.strip() == "SECURITY_ISSUE":
            st.warning("Security issue: query must be about data retrieval.")
            return

        if contains_forbidden_keywords(raw_response, FORBIDDEN_KEYWORDS):
            st.warning("Blocked: generated code contains restricted keywords.")
            return

        cleaned_code = strip_markdown(raw_response)
        st.session_state.cleaned_code = cleaned_code

        result = execute_generated_code(
            code=cleaned_code,
            source_df=st.session_state.source_df,
            timeout_seconds=TIMEOUT_SECONDS,
        )
        st.session_state.result = result
    except TimeoutError:
        st.session_state.execution_error = (
            "Query timed out (10s limit). Try a more specific query."
        )
    except ValueError as value_error:
        message = str(value_error)
        if "assign a result to 'ans'" in message:
            st.session_state.execution_error = "Model didn't return a result. Try rephrasing."
        else:
            st.session_state.execution_error = message
    except Exception as execution_error:
        st.session_state.execution_error = str(execution_error)


def render_chat_panel() -> None:
    st.subheader("Query")
    query = st.chat_input("Ask a question about your Excel data")
    if query:
        process_query(query)

    if st.session_state.result is not None:
        render_result(st.session_state.result)

    if st.session_state.execution_error:
        st.error(st.session_state.execution_error)
        st.info("Try rephrasing your query.")

    with st.expander("Debug Info"):
        st.write("Raw LLM response:")
        st.code(st.session_state.raw_llm_response or "[empty]", language="text")
        st.write("Cleaned code:")
        st.code(st.session_state.cleaned_code or "[empty]", language="python")
        st.write("Execution error:")
        st.code(st.session_state.execution_error or "[none]", language="text")


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    initialize_session_state()

    st.title(APP_TITLE)
    st.markdown(
        """
        <style>
        [data-testid="column"]:first-child {
            border-right: 1px solid #D0D7DE;
            padding-right: 1rem;
        }
        [data-testid="column"]:nth-child(2) {
            padding-left: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    left_col, right_col = st.columns([1, 4])

    with left_col:
        render_sidebar_panel()

    with right_col:
        render_chat_panel()


if __name__ == "__main__":
    main()