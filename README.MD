# NL2Pandas

NL2Pandas is a minimal Streamlit application that converts natural language queries into executable Pandas code using Gemini 2.5 Flash. It allows users to analyze and manipulate uploaded Excel data locally.

## Features
- **Excel Uploads Only**: Supports `.xlsx` files.
- **Two-Pane UI**: Metadata panel on the left, chat interface on the right.
- **Secure Execution**:
  - Forbidden keyword scan.
  - `exec` with empty builtins.
  - Threaded timeout (10 seconds).
  - Enforced `ans` contract for results.
- **Result Preview and Export**: View results in the app and export them as Excel files.
- **Debugging Tools**: Expandable debug panel for raw responses, cleaned code, and errors.

## Project Structure
- `ui.py`: Streamlit entrypoint and UI orchestration.
- `nl2pandas/config.py`: App constants and environment settings.
- `nl2pandas/data_observer.py`: File loading and metadata extraction.
- `nl2pandas/llm.py`: Gemini prompt and generation wrapper.
- `nl2pandas/security.py`: Markdown stripping, guardrails, and safe execution.
- `nl2pandas/exporters.py`: Excel export utility.

## Setup

### Prerequisites
- Python 3.8+
- [Google Cloud API Key](https://console.cloud.google.com/) with access to the Generative Language API.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/5AMEER/NL2Pandas.git
   cd NL2Pandas
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the `.env` file:
   ```bash
   touch .env
   ```
   Add your API key to the `.env` file:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage
1. Run the Streamlit app:
   ```bash
   streamlit run ui.py
   ```
2. Upload an Excel file and ask questions about your data in natural language.

## Notes
- Query handling is single-turn (no conversational history).
- Uploaded source DataFrame is kept immutable; execution always uses `df.copy()`.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Built with [Streamlit](https://streamlit.io/) and [Pandas](https://pandas.pydata.org/).
- Powered by [Google Gemini 2.5 Flash](https://cloud.google.com/).

## Future Scope

- **Conversational History**: Maintain a message thread so users can refine queries in context (e.g., "now sort that by date").
- **Multi-File Support**: Allow joining across two uploaded files.
- **Query History Panel**: Add a sidebar log of past queries and their results within a session.
- **LLM Provider Swap**: Abstract the generation layer to support other models like OpenAI or Anthropic.
- **CSV Export Option**: Provide an alternative export format alongside Excel.
- **Enhanced Security**: Implement stricter validation for generated code to prevent misuse.
- **Performance Optimization**: Improve handling of large datasets (e.g., 1M+ rows) for faster processing.
- **Customizable Prompts**: Allow users to modify the system prompt for tailored query handling.
- **Integration with Databases**: Extend support to query SQL databases directly.
- **Cloud Deployment**: Offer deployment options for hosting the app on platforms like AWS, GCP, or Azure.