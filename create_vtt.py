import math
import os


def format_time(timestamp):
    minutes, seconds = divmod(timestamp, 60)
    miliseconds = timestamp - math.floor(timestamp)
    return "{:02}:{:02.3f}".format(int(minutes), int(seconds) + miliseconds)


def create_vtts(
    target_dir, output_file_basename, transcribe_result, languages=["en", "es"]
):
    files = []
    for language in languages:
        text_field_name = "text"
        if language != "en":
            text_field_name = text_field_name + "_" + language
        file_name = os.path.join(target_dir, f"{output_file_basename}.{language}.vtt")
        with open(file_name, "w") as fout:
            fout.write("WEBVTT\n\n")

            for segment in transcribe_result["segments"]:
                fout.write(
                    f"{format_time(segment['start'])} --> {format_time(segment['end'])}\n{segment[text_field_name].strip()}\n\n"
                )
        files.append(file_name)
    return files
