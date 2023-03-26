from gtts import gTTS

from core.exceptions.app_exceptions import TextToAudioException

def create_audio(text, save_dir):
    try:
        language="en"
        output=gTTS(text=text, lang=language, slow=False)
        output.save("./audio_out.mp3")
        return True
    except Exception as e:
        raise TextToAudioException(str(e))


def get_audio_feedback(text):
    try:
        rs = create_audio(text, save_dir="/text_to_speech")
        if rs:
            return "./audio_out.mp3"
    except Exception as e:
        raise TextToAudioException(e)

