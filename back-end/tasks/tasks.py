from .weather.weather_task import WeatherTask


class Tasks:

    def __init__(self):
        self._tasks = []
        self.register_task(WeatherTask("Weather in Location", ["How is the weather", "How hot is it", "How many degrees is it"], "Get the weather information of a place only when the place is mentioned directly"))

    def set_tasks(self, tasks):
        self._tasks = tasks

    def get_tasks(self):
        return self._tasks

    def register_task(self, task):
        self.get_tasks().append(task)
