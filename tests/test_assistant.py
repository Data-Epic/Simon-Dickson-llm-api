import pytest
import os
import logging
from src.assistant import CustomerSupportAssistant
from src.config import AssistantConfig
from unittest.mock import patch
from requests.exceptions import RequestException


@pytest.fixture
def config():
    """Provide a test configuration."""
    return AssistantConfig()


@pytest.fixture
def setup_logging(tmp_path):
    """This is done to set up logging to a temporary file."""
    log_file = tmp_path / "test_assistant.log"
    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger = logging.getLogger('src.assistant')
    logger.setLevel(logging.INFO)
    logger.handlers = [handler]
    yield log_file
    handler.close()


@pytest.fixture
def assistant(config, setup_logging):
    """To create a CustomerSupportAssistant instance for testing."""
    # Skip API tests if GROQ_API_KEY is not set
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        pytest.skip("GROQ_API_KEY not set, skipping API tests")
    # Patch _setup_logging to prevent overriding test logging
    with patch.object(CustomerSupportAssistant, '_setup_logging', return_value=None):
        assistant = CustomerSupportAssistant(config)
        return assistant


def test_initialization_success(assistant, config):
    """Test successful initialization."""
    assert assistant.config == config
    assert assistant.client is not None
    assert isinstance(assistant.logger, logging.Logger)


def test_initialization_missing_api_key(monkeypatch, config):
    """Test initialization with missing API key."""
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    with pytest.raises(ValueError, match="GROQ_API_KEY environment variable not set"):
        CustomerSupportAssistant(config)


def test_validate_query_valid(assistant):
    """Test valid query validation."""
    assert assistant.validate_query("How do I reset my password?") is True


def test_validate_query_empty(assistant, setup_logging):
    """Test empty query validation."""
    assert assistant.validate_query("") is False
    assistant.logger.handlers[0].flush()
    with open(setup_logging) as f:
        assert "Empty query received" in f.read()


def test_validate_query_too_long(assistant, setup_logging):
    """Test query exceeding max length."""
    long_query = "a" * (assistant.config.MAX_QUERY_LENGTH + 1)
    assert assistant.validate_query(long_query) is False
    assistant.logger.handlers[0].flush()
    with open(setup_logging) as f:
        assert "Query exceeds max length" in f.read()


def test_prepare_prompt(assistant):
    """Test prompt preparation."""
    query = "How do I reset my password?"
    expected = (
        f"{assistant.config.SYSTEM_PROMPT}\n\n"
        f"Question: {query}"
    )
    assert assistant.prepare_prompt(query) == expected


def test_get_response_success(assistant):
    """Test successful API response with real API call."""
    prompt = assistant.prepare_prompt("How do I reset my password?")
    response, error = assistant.get_response(prompt)
    assert response is not None
    assert error is None
    assert "password" in response.lower()
    assistant.logger.handlers[0].flush()
    with open(assistant.config.LOG_FILE) as f:
        assert "Response received" in f.read()


def test_get_response_rate_limit(assistant, setup_logging):
    """Test handling of rate limit error (mocked, as real rate limit is hard to trigger)."""
    with patch.object(assistant.client.chat.completions, 'create', side_effect=Exception("Rate limit exceeded")):
        response, error = assistant.get_response("Test prompt")
        assert response is None
        assert "Rate limit exceeded" in error
        assistant.logger.handlers[0].flush()
        with open(setup_logging) as f:
            assert "Unexpected error" in f.read()


def test_get_response_network_error(assistant, setup_logging):
    """Test handling of network error (mocked)."""
    with patch.object(assistant.client.chat.completions, 'create', side_effect=RequestException("Network error")):
        response, error = assistant.get_response("Test prompt")
        assert response is None
        assert "Network issue" in error
        assistant.logger.handlers[0].flush()
        with open(setup_logging) as f:
            assert "Network error" in f.read()


def test_get_response_unexpected_error(assistant, setup_logging):
    """Test handling of unexpected error (mocked)."""
    with patch.object(assistant.client.chat.completions, 'create', side_effect=Exception("Unexpected error")):
        response, error = assistant.get_response("Test prompt")
        assert response is None
        assert "Unexpected error" in error
        assistant.logger.handlers[0].flush()
        with open(setup_logging) as f:
            assert "Unexpected error" in f.read()


def test_run_exit(assistant, capsys, monkeypatch):
    """Test run method with exit command."""
    from src.main import run_assistant
    monkeypatch.setattr("builtins.input", lambda _: "exit")
    run_assistant()
    captured = capsys.readouterr()
    assert "Welcome to the Customer Support Assistant" in captured.out
    assert "Goodbye!" in captured.out


def test_run_invalid_query(assistant, capsys, monkeypatch):
    """Test run method with invalid query."""
    from src.main import run_assistant
    inputs = ["", "exit"]
    input_iter = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_iter))
    run_assistant()
    captured = capsys.readouterr()
    assert "Invalid query" in captured.out


def test_run_api_success(assistant, capsys, monkeypatch):
    """Test run method with successful real API call."""
    from src.main import run_assistant
    inputs = ["How do I reset my password?", "exit"]
    input_iter = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_iter))
    run_assistant()
    captured = capsys.readouterr()
    assert "Assistant:" in captured.out
    assert "password" in captured.out.lower()
    assistant.logger.handlers[0].flush()
    with open(assistant.config.LOG_FILE) as f:
        assert "Response received" in f.read()