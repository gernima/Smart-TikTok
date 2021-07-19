from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
import speech_recognition
from moviepy.editor import *
from pathlib import Path


# video = os.path.abspath("Videos/101dalmatinec/101dalmatinec.avi").replace("\\", "/")
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
	VideoFileClip(video).subclip(t1, t2).write_videofile(f"Clips/{thread_name}/clip.mp4", fps=24, threads=10, codec="libx264")

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

# create_subclip(video, 180*0, 180*1, "thread_1")
# print(get_text(video, "thread_1"))
