# utils/ffmpeg_utils.py
import os
import subprocess

def burn_subtitles(video_path, srt_path, output_path, font_path=None):
    def escape_path(path):
        return path.replace('\\', '/').replace(':', '\\:').replace("'", "\\'")

    video_path_escaped = escape_path(video_path)
    srt_path_escaped = escape_path(srt_path)
    output_path_escaped = escape_path(output_path)

    if font_path:
        font_path_escaped = escape_path(font_path)
        subtitles_filter = f"subtitles='{srt_path_escaped}':force_style='FontFile={font_path_escaped}'"
    else:
        subtitles_filter = f"subtitles='{srt_path_escaped}'"

    command = ['ffmpeg', '-i', video_path, '-vf', subtitles_filter, '-c:a', 'copy', '-y', output_path]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print(f"Error burning subtitles into '{video_path}': {result.stderr}")
    else:
        print(f"Created video with subtitles: '{output_path}'")
