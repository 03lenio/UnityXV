import azure.cognitiveservices.speech as speechsdk

class NullAudioCallback(speechsdk.audio.PushAudioOutputStreamCallback):
    def __init__(self):
        super(NullAudioCallback, self).__init__()

    def write(self, data: bytes) -> int:
        # This will simply discard the audio data but not play it
        return len(data)