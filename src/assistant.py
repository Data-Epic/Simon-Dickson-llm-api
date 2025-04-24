import os
import logging
from typing import Optional, Tuple
from groq import Groq, GroqError
from requests.exceptions import RequestException
from .config import AssistantConfig


class CustomerSupportAssistant:
    """This handles customer inquiries using GroqCloud's deepseek-r1-distill-llama-70b model."""

    def __init__(self, config: AssistantConfig = AssistantConfig()):
        """
        Initialize the assistant with Groq client and logging.

        Args:
            config (AssistantConfig): Configuration settings for the assistant.
        """
        self.config = config
        self._setup_logging()
        self.logger = logging.getLogger(__name__)

        # Initialize Groq client
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            self.logger.error("GROQ_API_KEY environment variable not set")
            raise ValueError("GROQ_API_KEY environment variable not set")
        self.client = Groq(api_key=api_key)

    def _setup_logging(self):
        """To configure logging with file handler."""
        logging.basicConfig(
            filename=self.config.LOG_FILE,
            level=self.config.LOG_LEVEL,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def validate_query(self, query: str) -> bool:
        """
        Validate the user query.

        Args:
            query (str): The user's input query.
        """
        if not query:
            self.logger.warning("Empty query received")
            return False
        if len(query) > self.config.MAX_QUERY_LENGTH:
            self.logger.warning(f"Query exceeds max length: {len(query)} characters")
            return False
        return True

    def prepare_prompt(self, user_query: str) -> str:
        """
        Prepare the prompt for the Groq API.

        Args:
            user_query (str): The user's input query.
        """
        prompt = f"{self.config.SYSTEM_PROMPT}\n\nQuestion: {user_query}"
        self.logger.debug(f"Prepared prompt: {prompt[:100]}...")
        return prompt

    def get_response(self, prompt: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Send prompt to Groq API and retrieve response.

        Args:
            prompt (str): The formatted prompt to send.

        Returns:
            Tuple: (response, error_message). Response is None if an error occurs.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.config.MODEL,
                messages=[
                    {"role": "system", "content": self.config.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.TEMPERATURE,
                max_tokens=self.config.MAX_TOKENS
            )
            answer = response.choices[0].message.content.strip()
            self.logger.info(f"Response received: {answer[:100]}...")
            return answer, None
        except GroqError as e:
            self.logger.error(f"API error: {str(e)}")
            if "rate limit" in str(e).lower():
                return None, "Rate limit exceeded. Please try again later."
            return None, f"API error: {str(e)}"
        except RequestException as e:
            self.logger.error(f"Network error: {str(e)}")
            return None, "Network issue. Please check your connection and try again."
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return None, f"An unexpected error occurred: {str(e)}"