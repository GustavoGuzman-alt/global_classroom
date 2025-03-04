# utils/transcription.py
import os
import subprocess
import whisper

def transcribe_video(video_path, model_name="base"):
    # Load the Whisper model
    model = whisper.load_model(model_name)

    # Extract the audio from the video
    audio_path = os.path.splitext(video_path)[0] + ".mp3"
    command = ["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", "-y", audio_path]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Transcribe the audio
    result = model.transcribe(audio_path)

    # Generate SRT file
    srt_path = os.path.splitext(video_path)[0] + ".srt"
    with open(srt_path, "w", encoding="utf-8") as srt_file:
        for segment in result["segments"]:
            srt_file.write(f"{segment['id'] + 1}\n")
            start_time = format_timestamp(segment['start'])
            end_time = format_timestamp(segment['end'])
            srt_file.write(f"{start_time} --> {end_time}\n")
            srt_file.write(f"{segment['text'].strip()}\n\n")

    # Remove the temporary audio file
    os.remove(audio_path)
    print(f"Transcribed '{video_path}' to '{srt_path}' successfully.")

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"
