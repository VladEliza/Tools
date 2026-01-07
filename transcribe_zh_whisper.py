# filename: transcribe_zh_whisper.py
# Install: pip install -U openai-whisper torch
# Note: torch may need platform-specific wheels (see PyTorch install guide)

import sys
import whisper

def main(input_path="input.wav", model_size="small", language="zh"):
    """
    Transcribe a WAV to Chinese text using Whisper.
    model_size: tiny, base, small, medium, large
    - small/medium balance speed/accuracy; large is most accurate but heavy.
    """
    print(f"Loading Whisper model: {model_size}")
    model = whisper.load_model(model_size)

    print(f"Transcribing {input_path} with language='{language}' ...")
    result = model.transcribe(input_path, language=language, task="transcribe", fp16=False)
    # fp16=False ensures CPU compatibility; set True on CUDA GPUs

    print("---- Transcript ----")
    print(result["text"])

    # Optional: save SRT
    if "segments" in result:
        with open("output.srt", "w", encoding="utf-8") as srt:
            for i, seg in enumerate(result["segments"], start=1):
                def fmt(t):
                    h = int(t // 3600)
                    m = int((t % 3600) // 60)
                    s = int(t % 60)
                    ms = int((t - int(t)) * 1000)
                    return f"{h:02}:{m:02}:{s:02},{ms:03}"
                srt.write(f"{i}\n{fmt(seg['start'])} --> {fmt(seg['end'])}\n{seg['text'].strip()}\n\n")
        print("Saved subtitles to output.srt")

if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else "input.wav"
    main(input_path=input_path, model_size="small", language="zh")
