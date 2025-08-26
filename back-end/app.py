from flask import Flask, render_template, request, jsonify, send_file
from .tasks.weather.weather_task import WeatherTask
from .db.database_manager import DatabaseManager
from .util.utility import load_from_config
from .audio.synthesizer import Synthesizer
from .memories.brain import Brain
from .util.logger import Logger
from .tasks.tasks import Tasks
from .ai.gpt import GPT
import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
app = Flask(__name__)


@app.route('/debug')
def debug():
    return str("Yes, WeatherInLocation".count(",") == 1)


@app.route('/query', methods=['POST'])
def query():
    prompt = request.get_json()["prompt"]
    logger.logger.info(prompt)
    should_execute = tasks.smart_should_execute(prompt, local_gpt)
    if should_execute["Decision"] == "yes":
        task_str = should_execute["Task"]
        task = tasks.get_task_by_name(task_str)
        if tasks.is_task_registered(task):
            if isinstance(task, WeatherTask):
                task.set_task_str(prompt)
                return jsonify({"result": task.execute({"gpt": local_gpt})})
    # Old implementation, more stable but will eventually consume way more tokens and processing time as the amount of tasks go up
    """for task in tasks.get_tasks():
        logger.logger.info(task)
        if task.smart_should_execute(prompt, local_gpt):
            if isinstance(task, WeatherTask):
                task.set_task_str(prompt)
                return jsonify({"result": task.execute({"gpt": local_gpt})})"""
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


@app.route('/synthesize/<text>', methods=['GET'])
def synthesize(text):
    audio_data = synthesizer.synthesize_speech(load_from_config(config_path, "VoiceName"), text)
    if audio_data:
        audio_data.seek(0)  # Ensure the stream is at the beginning
        return send_file(audio_data, mimetype='audio/wav', as_attachment=True, download_name='synthesized_audio.wav')
    else:
        return "Speech synthesis failed.", 500

@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html", output_text="")


if __name__ == '__main__':
    config_path = os.path.join(os.getcwd(), "back-end", "config", "config.json")
    logger = Logger(config_path, "FlaskDebug")
    local_gpt = GPT(config_path)
    brain = Brain(config_path, local_gpt)
    database_manager = DatabaseManager()
    tasks = Tasks()
    synthesizer = Synthesizer(config_path)
    synthesizer.init_synthesizer()
    app.template_folder = os.path.join(BASE_DIR, 'front-end', 'templates')
    app.static_folder = os.path.join(BASE_DIR, 'front-end', 'static')
    app.run(debug=False)

