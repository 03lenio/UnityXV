from .weather.weather_task import WeatherTask
from ..ai.gpt import GPT
from .task import Task


class Tasks:

    def __init__(self):
        self._tasks = []
        self.register_task(WeatherTask("WeatherInLocation", ["How is the weather", "How hot is it", "How many degrees is it"], "Get the weather information of a place only when the place is mentioned directly"))

    def set_tasks(self, tasks):
        self._tasks = tasks

    def get_tasks(self):
        return self._tasks

    def map_tasks_to_names(self):
        map = ""
        for task in self.get_tasks():
            map += f"{task.get_name()}={task.get_description()}\n"
        return map

    def smart_should_execute(self, prompt: str, gpt: GPT):
        decision = gpt.query_gpt_for_task(f"You can only reply with two words seperated by comma, these are first either yes or no and second the name of the task as provided here\n:"
                               f"Does this prompt sound like a task? If it does which of these tasks is it based on these descriptions of task:\n"
                               f"{self.map_tasks_to_names()}\n"
                               f"{prompt}")
        if decision.count(",") == 1:
            return {"Decision": decision.split(",")[0].lower().strip(), "Task": decision.split(",")[1].strip()}
        else:
            print("Something went wrong")
            return {"Decision": "no", "Task": None}

    def get_task_by_name(self, name):
        for task in self.get_tasks():
            if task.get_name() == name:
                return task

    def is_task_registered(self, task: Task) -> bool:
        return task in self.get_tasks()

    def register_task(self, task):
        self.get_tasks().append(task)
