import whisperx
import os
import torch
import glob
import subprocess
import re

# --- CONFIGURATION ---
BASE_DIR = os.path.join(os.getcwd(), "youtube")
MODEL_NAME = "large-v3"
BATCH_SIZE = 4
CHUNK_SECONDS = 600

def clean_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def split_audio(input_file, chunks_dir):
    """Splits audio into chunks using ffmpeg."""
    os.makedirs(chunks_dir, exist_ok=True)
    pattern = os.path.join(chunks_dir, "chunk_%03d.mp3")
    # Use quiet mode for ffmpeg to reduce log noise
    cmd = f'ffmpeg -y -i "{input_file}" -f segment -segment_time {CHUNK_SECONDS} -c copy "{pattern}" -loglevel error'
    subprocess.run(cmd, shell=True, check=True)
    return sorted(glob.glob(os.path.join(chunks_dir, "chunk_*.mp3")))

def transcribe_all():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    
    # Find all mp3 files recursively
    mp3_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".mp3"):
                mp3_files.append(os.path.join(root, file))
    
    if not mp3_files:
        print("No MP3 files found to transcribe.")
        return

    print(f"Found {len(mp3_files)} MP3 files.")
    print(f"Loading Model: {MODEL_NAME} on {device}...")
    model = whisperx.load_model(MODEL_NAME, device, compute_type=compute_type, language="th")

    for input_audio in mp3_files:
        dir_name = os.path.dirname(input_audio)
        file_base = os.path.basename(input_audio).rsplit('.', 1)[0]
        final_output = os.path.join(dir_name, f"{file_base}.txt")
        
        if os.path.exists(final_output):
            print(f"Skipping: {file_base} (Transcript already exists)")
            continue

        chunks_folder = os.path.join(dir_name, f"chunks_{clean_filename(file_base)}")
        print(f"\n>>> Processing: {file_base}")
        
        try:
            # 1. Split
            chunk_files = split_audio(input_audio, chunks_folder)
            
            # 2. Transcribe Chunks
            for chunk in chunk_files:
                out_txt = chunk.replace(".mp3", ".txt")
                if os.path.exists(out_txt): continue
                
                print(f"  Transcribing {os.path.basename(chunk)}...")
                audio = whisperx.load_audio(chunk)
                result = model.transcribe(audio, batch_size=BATCH_SIZE, language="th", task="transcribe")
                
                with open(out_txt, "w", encoding="utf-8") as f:
                    for segment in result["segments"]:
                        f.write(f"{segment['text']}\n")
                
                if device == "cuda":
                    torch.cuda.empty_cache()

            # 3. Merge
            print(f"  Merging into {final_output}...")
            txt_files = sorted(glob.glob(os.path.join(chunks_folder, "chunk_*.txt")))
            with open(final_output, "w", encoding="utf-8") as outfile:
                for f_path in txt_files:
                    with open(f_path, "r", encoding="utf-8") as infile:
                        outfile.write(infile.read())
            
            # 4. Cleanup chunks
            print(f"  Cleaning up chunks...")
            for f in glob.glob(os.path.join(chunks_folder, "*")):
                os.remove(f)
            os.rmdir(chunks_folder)
            
            print(f"Done: {final_output}")
            
        except Exception as e:
            print(f"Error processing {file_base}: {e}")

if __name__ == "__main__":
    transcribe_all()
