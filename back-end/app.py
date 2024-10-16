from flask import Flask, render_template, request, jsonify
from .db.database_manager import DatabaseManager
from .memories.brain import Brain
from .util.logger import Logger
from .ai.gpt import GPT
import datetime
import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
app = Flask(__name__)


@app.route('/debug')
def debug():
    req = local_gpt.query_gpt("You are UnityXV, a personal AI assistant with a sense of humor and sarcasm, you are not cringe, and also a servant.", 800, 0.7, 0.95)
    logger.logger.debug(req)
    return req["choices"][0]["message"]["content"]


@app.route('/query', methods=['POST'])
def query():
    prompt = request.get_json()["prompt"]
    logger.logger.info(prompt)
    gpt_req = local_gpt.query_gpt(prompt)
    logger.logger.debug(gpt_req)
    if gpt_req:
        result = gpt_req
        logger.logger.info(result)
        logger.logger.info(local_gpt.get_history())
        logger.logger.info(len(local_gpt.get_history()))
        if (local_gpt.get_query_count() % 5) == 0:
            memories = database_manager.get_memories_from_db(5)
            context = brain.summarize_memories(memories)
            database_manager.save_context_to_db(context)
        if database_manager.get_non_obsolete_context_count() >= 5:
            contexts = database_manager.get_context_from_db(5)
            summarized_context = brain.summarize_context(contexts, database_manager)
            database_manager.save_context_to_db(summarized_context)
        return jsonify({"result": result})
    return jsonify({"result": "Sorry there is an issue communicating with the OpenAI API"})


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html", output_text="")


if __name__ == '__main__':
    config_path = os.path.join(os.getcwd(), "back-end", "config", "config.json")
    logger = Logger(config_path, "FlaskDebug")
    local_gpt = GPT(config_path)
    brain = Brain(config_path, local_gpt)
    database_manager = DatabaseManager()
    app.template_folder = os.path.join(BASE_DIR, 'front-end', 'templates')
    app.static_folder = os.path.join(BASE_DIR, 'front-end', 'static')
    app.run(debug=False)

