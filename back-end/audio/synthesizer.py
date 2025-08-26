from .null_audio_callback import NullAudioCallback
import azure.cognitiveservices.speech as speechsdk
from ..util.logger import Logger
from ..util import utility
import io


class Synthesizer:

    def __init__(self, config_path: str):
        self.config_path = config_path
        self._api_key = "blank"
        self._service_region = "blank"
        self._speech_config = None
        self._audio_output_config = None
        self.logger = Logger(config_path, "SyntheiszerDebug")

    def get_api_key(self):
        return self._api_key

    def set_api_key(self, value):
        self._api_key = value

    def get_service_region(self):
        return self._service_region

    def set_service_region(self, value):
        self._service_region = value

    def get_speech_config(self):
        return self._speech_config

    def set_speech_config(self, value):
        self._speech_config = value

    def get_audio_output_config(self):
        return self._audio_output_config

    def set_audio_output_config(self, value):
        self._audio_output_config = value

    def init_synthesizer(self):
        self.set_api_key(utility.load_from_config(self.config_path, "AzureSpeechAPIKey"))
        # Creates an instance of a speech config with specified subscription key and service region.
        self.set_service_region("westeurope")
        self.set_speech_config(speechsdk.SpeechConfig(subscription=self.get_api_key(), region=self.get_service_region()))
        self.logger.logger.info("Synthesizer initialized")

    def synthesize_speech(self, voice, text):
        # de-DE-SeraphinaMultilingualNeural
        self.get_speech_config().speech_synthesis_voice_name = voice
        # use the default speaker as audio output.
        null_audio_output_stream = speechsdk.audio.PushAudioOutputStream(NullAudioCallback())
        self.set_audio_output_config(speechsdk.audio.AudioOutputConfig(stream=null_audio_output_stream))
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.get_speech_config(), audio_config=self.get_audio_output_config())
        result = speech_synthesizer.speak_text_async(text).get()
        # Check result
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            self.logger.logger.info("Speech synthesized for text [{}]".format(text))
            # Collect the audio data from the stream
            audio_data = result.audio_data
            return io.BytesIO(audio_data)  # Return as a file-like object
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            self.logger.logger.error("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                self.logger.logger.error("Error details: {}".format(cancellation_details.error_details))
            return None
