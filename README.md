# Customer Support Assistant

A Python-based tool that uses the `deepseek-r1-distill-llama-70b` model on GroqCloud to handle customer inquiries interactively via the command line. The codebase is modularized into smaller, interrelated files for better readability and maintainability.

## Features

- Accepts user queries and provides helpful, courteous responses.
- Supports diverse inquiries (e.g., complaints, feedback, general questions).
- Comprehensive logging for inputs, responses, and errors.
- Enhanced error handling for API rate limits and network issues.
- Configurable model settings and prompt structure in `src/config.py`.
- Validates query length to prevent abuse.
- Comprehensive unit tests with real API calls in `tests/test_assistant.py`.
- Adheres to PEP8 standards with detailed documentation.

## Prerequisites

- Python 3.8+
- GroqCloud API key (sign up at [Groq Console](https://console.groq.com/))
- Required libraries: `groq`, `pytest`, `requests`

## Setup Instructions

1. **Clone the repository**:
```bash
git clone <repository-url>
cd customer-support-assistant
```

2. Create a Virtual Environment
**On Mac/Linux OS**
- Use the venv module to create a virtual environment (replace myenv with your preferred name):
```bash
python -m venv myenv
```
This creates a myenv directory containing the virtual environment.
- Activate the Virtual Environment to isolate your Python environment:
```bash
source myenv/bin/activate
```

**On Windows OS**
- Use the venv module to create a virtual environment (replace myenv with your preferred name):
```bash
python -m venv myenv
```
This creates a myenv directory containing the virtual environment.
- Activate the Virtual Environment to isolate your Python environment:
**In Command Prompt**:
```bash
myenv\Scripts\activate
```
**In PowerShell**:
```bash
.\myenv\Scripts\Activate.ps1
```
Your terminal prompt should change, indicating the virtual environment is active (e.g., (myenv)).

3. Install Dependencies
With the virtual environment active, install packages using pip:
```bash
pip install groq pytest requests
```

4. **Set the Groq API key:**
   Create a `.env` file in the root directory and add the API key:
```bash
GROQ_API_KEY=<string>
```

## Setup Instructions
- Ensure you’re in the project root directory:
```bash
cd /path/to/customer-support-assistant
```
- Run the assistant as a Python module:
```bash
python -m src.main
```
- Enter queries at the prompt or type exit to quit.
Note: Running python src/main.py directly may cause import errors due to relative imports. Use python -m src.main to ensure the src package is recognized correctly.

## Example Usage

Welcome to the Customer Support Assistant! Type 'exit' to quit.

Enter your query: How can I reset my password?

Assistant: To reset your password, please follow these steps:
1. Visit our website and click on "Login."
2. Select "Forgot Password?"
3. Enter your email address and click "Submit."
4. Check your email for a reset link and follow the instructions.

If you encounter any issues, feel free to contact us!

Enter your query: exit
Goodbye!

## Running Tests
To run the comprehensive test suite, which includes real API calls:

```bash
pytest tests/test_assistant.py -v
```

### Deactivate the Virtual Environment
When done, deactivate the virtual environment:
```bash
deactivate
```

#### Requirements:
- A valid `GROQ_API_KEY` environment variable must be set.
- An active internet connection is required for API tests.
- Tests for API errors (rate limits, network issues) are mocked to avoid unreliable conditions.

#### Future Improvements
- Add retry logic for rate-limited API calls.
- Implement conversation history for context-aware responses.
- Support multiple models or dynamic prompt templates in config.py.
- Integrate with CRM systems for enterprise use.
- Add performance metrics for response times and API usage.# Simon-Dickson-llm-api
