import logging


class AssistantConfig:
    """The configuration for the Customer Support Assistant."""
    MODEL = "deepseek-r1-distill-llama-70b"
    TEMPERATURE = 0.6
    MAX_TOKENS = 1024
    MAX_QUERY_LENGTH = 1000
    SYSTEM_PROMPT = (
        "You are a helpful and courteous customer support assistant. "
        "Provide accurate and polite responses to user inquiries."
    )
    LOG_FILE = "assistant.log"
    LOG_LEVEL = logging.INFO