import openai

from ..util import utility
from random import randint
from ..util import logger
import requests


class GPT:

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.is_initialized = False
        self._api_key = "blank"
        self._project_id = "blank"
        self._history = []
        self.logger = logger.Logger(self.config_path, "GPTDebug")
        self.init_gpt()

    def init_gpt(self):
        self.logger.logger.info("Initializing GPT")
        api_key = utility.load_from_config(self.config_path, "OpenAIApiKey")
        project_id = utility.load_from_config(self.config_path, "OpenAIProjectID")
        if (api_key and project_id) != "404":
            self.set_api_key(api_key)
            self.set_project_id(project_id)
            self.logger.logger.info("GPT initialized")
            self.is_initialized = True
        else:
            self.logger.logger.error("Config file could not be found!")

    def get_api_key(self):
        return self._api_key

    def set_api_key(self, value):
        self._api_key = value

    def get_project_id(self):
        return self._project_id

    def set_project_id(self, value):
        self._project_id = value

    def get_history(self):
        return self._history

    def set_history(self, value):
        self._history = value

    def append_history(self, message):
        self._history.append({"role": "user", "content": message})
        if len(self.get_history()) > 10:
            self._history.pop(0)

    def query_gpt(self, prompt: str, max_tokens: int, temperature: float, top_p: float) -> str:
        if self.is_initialized:
            if (randint(1, 10) == 1) or len(self.get_history()) == 0:
                # Sometimes we want to remind the GPT of it's "personality", OpenAI by default includes memory
                # But we do want to remind the GPT sometimes just to keep the experience fluent
                original_prompt = prompt
                prompt = f"You are UnityXV, a personal AI assistant with a sense of humor and sarcasm, you are not cringe, and also a servant.\n{original_prompt}"
                self.logger.logger.info("Reminding GPT of Unity's personality...")
            self.logger.logger.info("Querying GPT with prompt: {}".format(prompt))
            self.append_history(prompt)
            openai.api_key = self.get_api_key()
            openai.project = self.get_project_id()
            try:
                response = openai.chat.completions.create(
                    model="gpt-4",  # Or "gpt-3.5-turbo"
                    messages=self.get_history()
                )
                if response.choices[0]:
                    return response.choices[0].message.content
                else:
                    return "I was not able to respond to that, please try again."
            except requests.RequestException as e:
                self.logger.logger.error(f"Failed to make the request. Error: {e}")
        else:
            return "I could not query that since the GPT could not be initialized."


