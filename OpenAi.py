from logger import logger
import openai
from openai import OpenAI

class NoChoicesReturnedError(Exception):
    def __init__(self, message="No choices returned in the response", response=None, body=None):
        self.message = message
        self.response = response
        self.body = body
        super().__init__(self.message)

class OpenAi:
    def __init__(self, api_key, endpoint="https://api.openai.com/v1"):
        self.endpoint = endpoint
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            max_retries=5,
        )

    def chat(self, message):
        free_model = "deepseek/deepseek-r1:free"
        paid_model = "deepseek/deepseek-r1"
        logger.info(f"Sending message to OpenAI API: {message}")
        instructions = """You are flirting with a girl. You are charming and confident.
        Respond in a casual manner, keeping the response concise and without any breakdowns,
        translations, or additional explanations. Your mother tongue is Burmese/Myanmar.
        But you can also speak English and Japanese well."""
        messages = [
            {"role": "system", "content": instructions},
            {"role": "user", "content": message.strip()},
        ]
        try:
            logger.info(f"Sending API request to {self.endpoint}/chat.")
            logger.info(f"API request: {messages}")
            logger.info(f"Using free model: {free_model}")
            completion = self.client.chat.completions.create(
                model=free_model,
                messages=messages
            )
            logger.info(f"API request successful.")
            logger.info(f"API response: {completion}")
            # Check if the response contains an error
            if completion.choices is None:
                raise NoChoicesReturnedError()

            return completion.choices[0].message.content
        except openai.APIConnectionError as e:
            logger.error(f"The server could not be reached: {e}.")
        except (openai.APIStatusError, NoChoicesReturnedError) as e:
            logger.error(f"Another non-200-range status code was received: {e}.")
            try:
                logger.info(f"Retrying with paid model: {paid_model}")
                completion = self.client.chat.completions.create(
                    model=paid_model,
                    messages=messages
                )
                logger.info(f"API request successful.")
                logger.info(f"API response: {completion}")
                # Check if the response contains an error
                if completion.choices is None:
                    raise NoChoicesReturnedError()
                return completion.choices[0].message.content
            except openai.APIConnectionError as e:
                logger.error(f"The server could not be reached: {e}.")
            except (openai.APIStatusError, NoChoicesReturnedError) as e:
                logger.error(f"Paid model also failed with error: {e}.")
                raise e
