import whisper
import tempfile
import os
from moviepy.editor import VideoFileClip
from pathlib import Path



def transcribe_video(input_video_file, whisper_model):
    model = whisper.load_model(whisper_model)
    print('Whisper model loaded')
    
    with tempfile.TemporaryDirectory() as tmpdirname:
        audio_file_name = os.path.join(tmpdirname, Path(input_video_file).stem + '.mp3')
        extract_audio(input_video_file, audio_file_name)
        transcribe_result = model.transcribe(audio_file_name, verbose=False)

    return transcribe_result

def extract_audio(video_file, audio_file):
    video = VideoFileClip(video_file)
    audio = video.audio
    audio.write_audiofile(audio_file, codec='mp3')