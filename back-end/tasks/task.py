from ..ai.gpt import GPT


class Task:

    def __init__(self, name, keywords: list[str], description: str):
        self.name = name
        self._task_str = ""
        self.keywords = keywords
        self.description = description

    def execute(self, parameters=None):
        pass

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_keywords(self):
        return self.keywords

    def set_keywords(self, keywords):
        self.keywords = keywords

    def set_task_str(self, task_str):
        self._task_str = task_str

    def get_task_str(self):
        return self._task_str

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description

    # This implementation is cheap and fast but may be prone to errors
    def should_execute(self, prompt: str) -> bool:
        for keyword in self.keywords:
            if keyword.lower() in prompt.lower():
                return True

    # This implementation is more stable but it takes processing time to run this for every task on every prompt
    def smart_should_execute(self, prompt: str, gpt: GPT) -> bool:
        return "yes" in gpt.query_gpt_for_task(f"You can only respond with yes or no. Does this description of a task:\n'{self.description}'\n align with this prompt:\n '{prompt}'").lower()

    def extract_task_params(self, prompt: str, gpt: GPT):
        return gpt.query_gpt_for_task(f"{prompt}:\n{self.get_task_str()}")
