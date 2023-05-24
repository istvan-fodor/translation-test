#!/usr/bin/env python
# coding: utf-8
from pathlib import Path
import os
import argparse
import yaml
from create_vtt import create_vtts
from transcribe import transcribe_video
from translate import translate_whisper_transcript

if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description="Process some video and audio data.")

    # Add the arguments
    parser.add_argument(
        "--output-dir",
        default="output",
        type=str,
        help='The directory where the script should save its output. This defaults to "output" if not specified.',
    )

    parser.add_argument(
        "--input-video-file",
        required=True,
        type=str,
        help="The path to the video file that the script should process. This is mandatory and has no default value.",
    )

    parser.add_argument(
        "--whisper-model",
        default="small.en",
        type=str,
        help='The name of the Whisper ASR model that the script should use for transcription. This defaults to "small.en" if not specified.',
    )

    parser.add_argument(
        "--translation-model",
        default="facebook/m2m100_1.2B",
        type=str,
        help='The name of the translation model that the script should use for translating the transcription into Spanish. This defaults to "facebook/m2m100_1.2B" if not specified.',
    )

    parser.add_argument(
        "--languages",
        nargs="+",
        default=["en", "es"],
        help="The languages that the script should use for transcription and translation. This defaults to English and Spanish ('en es' on the command line) if not specified.",
    )

    args = parser.parse_args()

    output_dir = args.output_dir
    input_video_file = args.input_video_file
    whisper_model = args.whisper_model
    translation_model = args.translation_model
    languages = args.languages
    transcription_file = os.path.join(output_dir, Path(input_video_file).stem + ".yaml")

    os.makedirs(output_dir, exist_ok=True)

    print("Processing video:", input_video_file)

    print("Transcribing video")
    transcribe_result = transcribe_video(input_video_file, whisper_model)

    with open(transcription_file, "w", encoding="utf-8") as f:
        f.write(yaml.dump(transcribe_result, default_flow_style=False, indent=2))

    print("Translating video")

    for language in languages:
        if language == "en":
            continue
        translate_result = translate_whisper_transcript(
            transcription_file, language=language, model=translation_model
        )

        for i, segment in enumerate(transcribe_result["segments"]):
            segment[f"text_{language}"] = translate_result[i]

    print("Creating VTT files")
    files = create_vtts(
        output_dir,
        Path(input_video_file).stem,
        transcribe_result,
        languages=languages,
    )
    print("VTT files created:", files)
    print("Done")
