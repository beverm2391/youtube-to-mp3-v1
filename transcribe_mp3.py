import argparse
import os
import requests
import openai
from dotenv import load_dotenv
import random

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_all_mp3s(path: str):
    if not os.path.exists(path): # if path doesn't exist, raise error
        raise ValueError(f"Path {path} does not exist")
    
    if os.path.isdir(path): # if is dir
        file_paths = [fpath for fpath in os.listdir(path) if fpath.endswith(".mp3")] # get all mp3 files
        
        if len(file_paths) == 0: # if none, raise error
            raise ValueError("No mp3 files found in directory")
        # TODO make async
        return '\n\n'.join([transcribe_mp3(fpath) for fpath in file_paths]) # transcribe all mp3 files
    
    elif os.path.isfile(path): # if is file
        if not path.endswith(".mp3"): # if not mp3, raise error
            raise ValueError("File path must be an mp3 file")
        return transcribe_mp3(path) # transcribe mp3 file

def transcribe_mp3(path: str, model: str = "whisper-1", parse=True):
    def _get(file_bytes):
        return openai.Audio.transcribe(
            model,
            file_bytes,
        )

    def _parse(transcript): return transcript['text']

    with open(path, "rb") as f:
        file_bytes = f.read()
    
    try:
        transcript = _get(file_bytes)
    except Exception as e:
        print(f"Error transcribing {path} in whisper API call")
        print(e)
        return None
    
    if parse:
        return _parse(transcript)
    return transcript

def save_transcript(transcript: str, args_path: str):
    def _rand6(): return random.randint(0, 999999)

    filename = f"{args_path}_transcript_{_rand6}.txt"
    output_dir = "transcripts"
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    output_path = os.path.join(output_dir, filename)
    with open(output_path, "w") as f:
        f.write(transcript)

    print(f"Saved transcript to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe mp3")
    parser.add_argument("path", type=str, help="The folder of file path")
    args = parser.parse_args()

    result = transcribe_all_mp3s(args.path)
    save_transcript(result, args.path)