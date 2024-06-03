import azure.cognitiveservices.speech as speechsdk
from config import *


class GetAudio:
    def __init__(self):
        pass

    def get_ssml_audio(self, file_name, text):
        # path = projectPath + 'data/audio/'
        # file_path = os.path.join(path, file_name)
        file_path = file_name

        # Set up the Text-to-Speech client
        speech_config = speechsdk.SpeechConfig(
            subscription=AZURE_AI_SERVICES_KEY,
            region=AZURE_SPEECH_REGION,
        )

        # The language of the voice that speaks.
        speech_config.speech_synthesis_voice_name = AZURE_US_FEMALE_MODEL
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        # en-US-CoraNeural
        # en-GB-RyanNeural
        voice_name = "en-US-CoraNeural"

        ssml_text = f"""
        <speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xml:lang="en-US">
            <voice name={voice_name}>
                {text}
            </voice>
        </speak>
        """

        # Convert the SSML to speech and save to a file
        result = speech_synthesizer.speak_ssml_async(ssml_text).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            audio_data = result.audio_data
            with open(file_path, "wb") as file:
                file.write(audio_data)

        print(file_path)
        return file_path

    def generateAudio(self, file, text):
        fileAdd = file
        speech_config = speechsdk.SpeechConfig(
            subscription=AZURE_AI_SERVICES_KEY,
            region=AZURE_SPEECH_REGION,
        )
        voice_name="en-US-AndrewNeural"

        audio_config = speechsdk.audio.AudioOutputConfig(filename=fileAdd)
        speech_config.speech_synthesis_voice_name = voice_name
        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=audio_config
        )

        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

        if (
            speech_synthesis_result.reason
            == speechsdk.ResultReason.SynthesizingAudioCompleted
        ):
            print("Speech synthesized for text [{}]".format(text))
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print(
                        "Error details: {}".format(cancellation_details.error_details)
                    )
                    print("Did you set the speech resource key and region values?")

        return fileAdd
