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
        self.histories = {}
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            max_retries=5,
        )
   
    def append_to_history(self, person_id, message):
        if person_id not in self.histories:
            self.histories[person_id] = []
        logger.info(f"Appending message to conversation history for {person_id}: {message}")
        self.histories[person_id] = self.manage_conversation_history(self.histories[person_id], message)

    @staticmethod
    def manage_conversation_history(history, new_message, max_characters=35000):
        history.append(new_message)
        total_characters = sum(len(message['content']) for message in history)
        
        while total_characters > max_characters:
            logger.info(f"Conversation history exceeds {max_characters} characters. Removing the oldest message.")
            history.pop(0)
            total_characters = sum(len(message['content']) for message in history)
        
        return history

    def chat(self, person_id, message):
        free_model = "deepseek/deepseek-r1:free"
        paid_model = "deepseek/deepseek-r1"
        logger.info(f"Sending message to OpenAI API: {message}")
        instructions = """You are having a conversation. You do not want the conversation to end,
        so you ask questions about their interests and talk about them to keep the conversation going.
        Respond in a casual manner, keeping the response smooth and interesting. 
        Your mother tongue is Burmese/Myanmar. But you can also speak English and Japanese well."""

        system_message = {"role": "system", "content": instructions}

        # Append the new message to the person's conversation history
        self.append_to_history(person_id, {"role": "user", "content": message})
        logger.info(f"Conversation history for {person_id}: {self.histories[person_id]}")

        # Prepare the conversation history for the API call
        conversation_history = [system_message] + self.histories[person_id]
        logger.info(f"Conversation history: {conversation_history}")

        try:
            logger.info(f"Sending API request to {self.endpoint}/chat.")
            logger.info(f"Using free model: {free_model}")
            completion = self.client.chat.completions.create(
                model=free_model,
                messages=conversation_history
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
                    messages=conversation_history
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
