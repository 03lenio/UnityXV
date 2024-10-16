class Memory:

    def __init__(self, memory, timestamp):
        self._memory = memory
        self._timestamp = timestamp

    def set_memory(self, value):
        self._memory = value

    def get_memory(self):
        return self._memory

    def set_timestamp(self, value):
        self._timestamp = value

    def get_timestamp(self):
        return self._timestamp
