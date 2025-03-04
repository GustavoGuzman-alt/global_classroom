# processors/video_processor.py

import os
import tempfile
import shutil
from utils.transcription import transcribe_video
from utils.translation import translate_srt_file
from utils.ffmpeg_utils import burn_subtitles

def process_single_video(video_path, target_language='ne'):
    temp_dir = tempfile.mkdtemp()
    try:
        # Copy the original video to a temporary directory.
        shutil.copy(video_path, temp_dir)
        # Process all videos in the temporary directory.
        process_videos_in_folder(temp_dir, target_language)
        base, ext = os.path.splitext(os.path.basename(video_path))
        # Only copy the final video (with burned subtitles) to the output.
        final_video = os.path.join(temp_dir, f"{base}_{target_language}.mp4")
        if os.path.exists(final_video):
            shutil.copy(final_video, os.path.dirname(video_path))
    finally:
        shutil.rmtree(temp_dir)
    return "Video processing completed successfully."

def process_videos_in_folder(folder_path, target_language='ne'):
    model_name = "base"
    # Set your font path if needed for burning subtitles.
    font_path = "C:\\Windows\\Fonts\\NotoSansDevanagari-Regular.ttf"
    for filename in os.listdir(folder_path):
        if filename.endswith((".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv")):
            video_path = os.path.join(folder_path, filename)
            try:
                transcribe_video(video_path, model_name)
                # Translate the SRT file using the specified target language.
                srt_path = translate_srt_file(os.path.splitext(video_path)[0] + ".srt", target_language=target_language)
                # Burn the translated subtitles into a new video file.
                burn_subtitles(video_path, srt_path, os.path.splitext(video_path)[0] + f"_{target_language}.mp4", font_path)
            except Exception as e:
                print(f"Error processing '{filename}': {e}")
