import sys
from .assistant import CustomerSupportAssistant

def run_assistant():
    """To run the interactive loop to handle user queries."""
    assistant = CustomerSupportAssistant()
    print("Welcome to the Customer Support Assistant! Type 'exit' to quit.")
    assistant.logger.info("Assistant started")

    try:
        while True:
            user_query = input("\nEnter your query: ").strip()
            assistant.logger.info(f"User query: {user_query}")

            if user_query.lower() == 'exit':
                print("Goodbye!")
                assistant.logger.info("Assistant terminated by user")
                break

            if not assistant.validate_query(user_query):
                print(
                    "Invalid query. Ensure it is non-empty and within "
                    f"{assistant.config.MAX_QUERY_LENGTH} characters."
                )
                continue

            prompt = assistant.prepare_prompt(user_query)
            response, error = assistant.get_response(prompt)
            if error:
                print(f"Error: {error}")
            else:
                print(f"\nAssistant: {response}")

    except KeyboardInterrupt:
        print("\nAssistant interrupted. Exiting...")
        assistant.logger.info("Assistant interrupted by user")
    except Exception as e:
        assistant.logger.error(f"Runtime error: {str(e)}")
        print(f"Error: {str(e)}")
    finally:
        assistant.logger.info("Assistant shutdown")


def main():
    """The main entry point for the assistant."""
    try:
        run_assistant()
    except ValueError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to start assistant: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()