from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
import speech_recognition
from moviepy.editor import *
from pathlib import Path
import subprocess

video = os.path.abspath("Videos/101dalmatinec.avi").replace("\\", "/")
recognizer = speech_recognition.Recognizer()


def get_duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return float(result.stdout)


def create_subclip(video, t1, t2, thread_name):
    Path(f"Clips/{thread_name}/").mkdir(parents=True, exist_ok=True)
    clip = VideoFileClip(video).subclip(t1, t2)
    clip.write_videofile(f"Clips/{thread_name}/clip.mp4", fps=24, threads=20, codec="libx264")
    clip.reader.close()
    clip.audio.reader.close_proc()


def resize(video, width=1080, height=1920):
    clip = VideoFileClip(video)
    size = int(clip.h * 1.1 // 2)
    clip_with_borders = clip.margin(top=size, bottom=size)
    clip_with_borders.write_videofile(video, fps=24, threads=20, codec="libx264")
    clip.reader.close()
    clip.audio.reader.close_proc()


def add_text(video, text, font="Calibri", color="white", fontsize=50):
    clip = VideoFileClip(video)
    # Generate a text clip
    txt_clip = TextClip(text, fontsize=fontsize, color=color, font=font)
    # setting position of text in the center and duration will be 10 seconds
    txt_clip = txt_clip.set_position(("center", clip.h * 0.2)).set_duration(clip.duration)
    # Overlay the text clip on the first video clip
    final = CompositeVideoClip([clip, txt_clip])
    final.write_videofile(video, fps=24, threads=20, codec="libx264")
    clip.reader.close()
    clip.audio.reader.close_proc()


def delete_video(video):
    os.remove(video)


def get_text(video, thread_name):
    clip = f"Clips/{thread_name}/clip.mp4"
    wav_path = f"Clips/{thread_name}/audio.wav"
    clip = VideoFileClip(clip)
    clip.audio.write_audiofile(wav_path)
    audio = speech_recognition.AudioFile(wav_path)
    with audio as source:
        audio_file = recognizer.record(source)
    return recognizer.recognize_google(audio_file, language="ru-RU")


t = 30
create_subclip(video, t * 10, t * 11, "thread_1")
resize(f"Clips/thread_1/clip.mp4")
add_text(f"Clips/thread_1/clip.mp4", "Part #")
# print(get_text(video, "thread_1"))
