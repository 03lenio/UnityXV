from .utility import load_from_config
import logging
import os


class Logger:

    def __init__(self, config_path: str, name: str) -> None:
        self.config_path = config_path
        self._log_dir = "/"
        self.name = name
        self.logger = self.init_logger()

    def init_logger(self):
        log_dir = load_from_config(self.config_path, "LogDirectory")
        self.set_log_dir(log_dir)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        # Create a logger
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)  # Set the default logging level to DEBUG
        # Create a file handler that logs messages to a file
        file_handler = logging.FileHandler(f'{log_dir}/app.log')
        file_handler.setLevel(logging.DEBUG)  # Log everything to the file
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        # Add the handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        return logger

    def set_log_dir(self, value: str) -> None:
        self._log_dir = value

    def get_log_dir(self):
        return self._log_dir
