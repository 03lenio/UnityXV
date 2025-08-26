from ..db.database_manager import DatabaseManager
from ..memories.memory import Memory
from ..util import utility
from random import randint
from ..util import logger
import requests
import openai
import time


class GPT:

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.is_initialized = False
        self._api_key = "blank"
        self._project_id = "blank"
        self._history = []
        self._query_count = 0
        self.database_manager = DatabaseManager()
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

    def get_query_count(self):
        return self._query_count

    def set_query_count(self, value):
        self._query_count = value

    def increment_query_count(self):
        self._query_count += 1

    def append_history(self, message):
        self._history.append({"role": "user", "content": message})
        memory = Memory(message, time.time())
        self.database_manager.save_memory_to_db(memory)
        if len(self.get_history()) > 5:
            self._history.pop(0)

    def query_gpt(self, prompt: str) -> str:
        if self.is_initialized:
            if randint(1, 10) == 1:
                # Sometimes we want to remind the GPT of it's "personality", OpenAI by default includes memory
                # But we do want to remind the GPT sometimes just to keep the experience fluent
                original_prompt = prompt
                prompt = f"You are UnityXV, a personal AI assistant with a sense of humor and sarcasm, you are not cringe, and also a servant.\n{original_prompt}"
                self.logger.logger.info("Reminding GPT of Unity's personality...")
            contexts = self.database_manager.get_context_from_db(5)
            context_count = 0
            for context in contexts:
                context_count += 1
                context_elem = context.get("context")
                self.logger.logger.info(f"Loading context:\n{context_elem}")
                self.get_history().append({"role": "user", "content": f"Keep this information in mind when replying and apply it if you think it adds to the conversation; reply like a human would: {context_elem}"})
            if context_count == 1:
                self.get_history().append({"role": "user", "content": "Ignore the above message, just use it as a guide on how to interact with the user, the following chat log represents the last 5 messages the user sent."})
            if len(self.get_history()) == 0:
                previous_history = self.database_manager.get_memories_from_db_str(5)
                messages = []
                for message in previous_history:
                    messages.append({"role": "user", "content": message})
                self.set_history(messages)
                self.logger.logger.info("Restoring last 10 memories")
                self.logger.logger.debug(self.get_history())
            self.logger.logger.info("Querying GPT with prompt: {}".format(prompt))
            self.append_history(f"give a brief reply in about 80 tokens:\n{prompt}")
            openai.api_key = self.get_api_key()
            openai.project = self.get_project_id()
            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",  # Or "gpt-3.5-turbo" # CHANGED # Was gpt-4
                    messages=self.get_history(),
                    max_tokens=80
                )
                if response.choices[0]:
                    self.increment_query_count()
                    return response.choices[0].message.content
                else:
                    return "I was not able to respond to that, please try again."
            except requests.RequestException as e:
                self.logger.logger.error(f"Failed to make the request. Error: {e}")
        else:
            return "I could not query that since the GPT could not be initialized."

    def query_gpt_for_task(self, prompt: str) -> str:
        if self.is_initialized:
            # Maybe implement memories of these for song recommendations or sth
            openai.api_key = self.get_api_key()
            openai.project = self.get_project_id()
            prompt_to_submit = [{"role": "user", "content": prompt}]
            try:
                response = openai.chat.completions.create(
                    model="gpt-4",  # Or "gpt-3.5-turbo"
                    messages=prompt_to_submit,
                    max_tokens=20,
                    temperature=0.3
                )
                if response.choices[0]:
                    self.logger.logger.info(response.choices[0].message.content)
                    return response.choices[0].message.content
                else:
                    return "I was not able to respond to that, please try again."
            except requests.RequestException as e:
                self.logger.logger.error(f"Failed to make the request. Error: {e}")
        else:
            return "I could not query that since the GPT could not be initialized."

    def query_gpt_with_messages(self, messages: list[dict]) -> str:
        if self.is_initialized:
            self.logger.logger.info("Querying GPT with Messages: {}".format(messages))
            openai.api_key = self.get_api_key()
            openai.project = self.get_project_id()
            try:
                response = openai.chat.completions.create(
                    model="gpt-4",  # Or "gpt-3.5-turbo"
                    messages=messages
                )
                if response.choices[0]:
                    return response.choices[0].message.content
                else:
                    return "I was not able to respond to that, please try again."
            except requests.RequestException as e:
                self.logger.logger.error(f"Failed to make the request. Error: {e}")
        else:
            return "I could not query that since the GPT could not be initialized."


