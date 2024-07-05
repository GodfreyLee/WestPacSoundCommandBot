from gtts import gTTS
from pydub import AudioSegment
import io

# Texts to convert to speech
texts = [
    "Hi, How can I help you today?",
    "Do you want to transfer $500 to Peter?",
    "Transaction done",
    "Transaction done",
    "Thanks for choosing WestPac. Have a nice one."
]

# Generate speech segments
segments = []
pause_duration = 6000  # 6 seconds in milliseconds

# Initial pause
segments.append(AudioSegment.silent(duration=pause_duration))

for text in texts:
    tts = gTTS(text)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    speech = AudioSegment.from_file(fp, format="mp3")
    segments.append(speech)
    segments.append(AudioSegment.silent(duration=pause_duration))

# Combine segments
combined = AudioSegment.empty()
for segment in segments:
    combined += segment

# Save the final audio to a file
output_file = "combined_speech.mp3"
combined.export(output_file, format="mp3")
