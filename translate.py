from transformers import pipeline
from tqdm import tqdm
import torch
import yaml



def translate_whisper_transcript(transcription_file, language, model='facebook/m2m100_1.2B', batch_size = 10):

    if torch.cuda.is_available():
        device = torch.cuda.current_device()
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = -1

    pipe = pipeline(task='text2text-generation', model=model, device = device)
    
    with open(transcription_file, 'r') as stream:
        try:
            transcript = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            raise exc
    
    max_count = len(transcript['segments'])
    translated = []
    print("Translating ", max_count, " English sentences" )
    for i in tqdm(range(0, max_count, batch_size)):
        batch = [segment['text'] for segment in transcript['segments'][i:i+batch_size]]
        #print("Translating sentences", i, "to", i+len(batch)-1)
        translated_batch = pipe(batch, forced_bos_token_id=pipe.tokenizer.get_lang_id(lang=language))
        translated.extend([text['generated_text'] for text in translated_batch])

    return translated
