Utilities for transcription and translation
=========================================

This Python script a solution to process video files, transcribe the audio into multiple languages, and produce WebVTT (Web Video Text Tracks) files for each language transcription.

The script starts by transcribing the audio of the input video file using OpenAI's Whisper ASR system. Then it translates the transcription into a list of languages provided by the user, using the specified translation model. Finally, it generates WebVTT files for the transcriptions in all languages.

This script is highly flexible, allowing you to specify the directory for output files, the Whisper ASR model for transcription, the translation model, and the languages for transcription and translation. The default output directory is output, the default Whisper ASR model is small.en, and the default translation model is facebook/m2m100_1.2B. By default, the script transcribes and translates into English and Spanish.

## Pre-requisites

1. `ffmpeg` installed and awailable on the PATH 
2. Python 3 
3. Install CUDA driver if you have an Nvidia graphics card.

## Installation

1. On the command line navigate to this folder
1. Create python environment: `python -m venv venv`
1. Activate the environment: 
    1. On Linux/Mac: `source venv/bin/activate`
    1. On Windows: `venv/Scripts/activate`
1. Install regular requirements: `pip install -r requirements.txt`
1. Install torch requirements: 
    1. On CUDA enabled computer: `pip install -r torch_requirements.txt --index-url https://download.pytorch.org/whl/cu118`
        
        a. Run the following to check if CUDA is available: `python -c 'import torch; print("CUDA is available" if torch.cuda.is_available() else "CUDA is not available")'`
        
        b. If CUDA is not available, double check your video driver and CUDA driver installation.
    1. Without CUDA: `pip install -r torch_requirements.txt`

## Usage
The script takes five command-line arguments:

* `--output-dir`: The directory where the script should save its output. This defaults to `output` if not specified.

* `--input-video-file`: The path to the video file that the script should process. This is mandatory and has no default value.

* `--whisper-model`: The name of the Whisper ASR model that the script should use for transcription. This defaults to `small.en` if not specified.

* `--translation-model`: The name of the translation model that the script should use for translating the transcription into Spanish. This defaults to `facebook/m2m100_1.2B` if not specified.

* `--languages`: The languages that the script should use for transcription and translation. This defaults to English and Spanish ('en es' on the command line) if not specified.

You can run the script from the command line as follows:

```bash
python speech_rec.py --output-dir path_to_output_dir --input-video-file path_to_input_video --whisper-model whisper_model_name --translation-model translation_model_name --languages language_code1 language_code2
```

Replace the placeholders path_to_output_dir, path_to_input_video, whisper_model_name, translation_model_name and language_code with your desired values.

### Example

To process the video file example.mp4 using the default Whisper, translation model and languages, and save the output in the my_output directory, you would use the following command:

```bash
python speech_rec.py --output-dir my_output --input-video-file example.mp4 --languages en es
```

### Output
The script will generate several output files in the output directory:

* A YAML file containing the transcription of the video in English.
* Two VTT files for the transcriptions in English and Spanish, respectively. These files can be used for displaying subtitles or captions in a video player that supports the WebVTT format.
* The script prints out status messages as it processes the video, and it will tell you the names of the VTT files when it's done.



