import os
import pyaudio
import wave
from google.cloud import speech
import io
import vertexai
from vertexai.generative_models import GenerativeModel

# Set the environment variable within the script
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "account.json"

def record_audio(filename, duration=5):
    # Set up parameters
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open a new stream
    print("Recording...")
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []

    # Record for the specified duration
    for i in range(0, int(fs / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate the PyAudio object
    p.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("Recording finished.")

def transcribe_audio(audio_file_path):
    client = speech.SpeechClient()

    with io.open(audio_file_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='en-US'
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "

    return transcript.strip()

def main():
    audio_file = "audio/recorded_audio.wav"
    project_id = "Type your project id"
    vertexai.init(project=project_id, location="us-central1")

    model = GenerativeModel(model_name="gemini-1.5-flash-001")

    while True:
        record_audio(audio_file, duration=5)
        transcription = transcribe_audio(audio_file)
        print("Transcription:", transcription)

        response = model.generate_content(transcription)
        print(response.text)
        print("Say the end to end the service")

        if "the end" in transcription.lower():
            print("Thank you for choosing the service.")
            break

if __name__ == "__main__":
    main()
