from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os

video = os.path.abspath("Videos/101dalmatinec/101dalmatinec.avi").replace("\\", "/")
print(video)

def get_duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

def get_subcLip(video, t1, t2, thread_name):
	return ffmpeg_extract_subclip(video, t1, t2, targetname=f"Clips/{thread_name}.avi")

def delete_video(video):
	os.remove(video)

print(get_subcLip(video, 0, 180, "thread_1"))
