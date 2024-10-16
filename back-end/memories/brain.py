from ..db.database_manager import DatabaseManager
from ..util.logger import Logger
from .memory import Memory
from ..ai.gpt import GPT
import datetime


class Brain:

    def __init__(self, config_path, gpt):
        self.config_path = config_path
        self.gpt = gpt
        self.logger = Logger(config_path, "BrainDebug")

    def summarize_memories(self, memories: list[dict]) -> str:
        to_summarize = [{"role": "user", "content": "You are an AI assistant called UnityXV that is supposed to memorize details about it's user, summarize this chatlog that gives context about the user."}]
        for memory in memories:
            memory_str = memory.get("memory")
            memory_time = memory.get("timestamp")
            time_str = datetime.datetime.utcfromtimestamp(memory_time).strftime('%d-%m-%Y %H:%M')
            memory_str = f"{memory_str} - Memory was made at {time_str}"
            to_summarize.append({"role": "user", "content": memory_str})
        self.logger.logger.info(to_summarize)
        return self.gpt.query_gpt_with_messages(to_summarize)

    def summarize_context(self, contexts: list[dict], database_manager: DatabaseManager) -> str:
        to_summarize = [{"role": "user", "content": "You are an AI assistant called UnityXV that is supposed to memorize details about it's user, you already collected some context about the user. Summarize the following context further and pick out the key information."}]
        for context in contexts:
            if not context.get("obsolete"):
                context_str = context.get("context")
                context_time = context.get("timestamp")
                time_str = datetime.datetime.utcfromtimestamp(context_time).strftime('%d-%m-%Y %H:%M')
                context_str = f"{context_str} - Context was saved at {time_str}"
                to_summarize.append({"role": "user", "content": context_str})
                database_manager.mark_context_obsolete(context_time)
        self.logger.logger.info(to_summarize)
        return self.gpt.query_gpt_with_messages(to_summarize)

