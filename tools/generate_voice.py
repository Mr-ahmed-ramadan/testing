"""Pre-record an episode's voice lines with Kokoro (free, open-source neural TTS).

Usage: python3 tools/generate_voice.py <episode_dir> <model_dir> [line_key ...]
  A line is either a string (spoken in the default voice) or {"text": ..., "voice": ...}.
  episode_dir contains lines.json; mp3 files are written to <episode_dir>/audio/
  model_dir contains kokoro-v1.0.onnx and voices-v1.0.bin from
  https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0
Requires: pip install kokoro-onnx soundfile, and ffmpeg.
"""
import json, pathlib, subprocess, sys, tempfile
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

ep, models = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
cfg = json.loads((ep / "lines.json").read_text())
k = Kokoro(str(models / "kokoro-v1.0.onnx"), str(models / "voices-v1.0.bin"))
out = ep / "audio"; out.mkdir(exist_ok=True)
only = set(sys.argv[3:])  # optional: regenerate only these line keys
for key, line in cfg["lines"].items():
    if only and key not in only:
        continue
    text, voice = (line, cfg["voice"]) if isinstance(line, str) else (line["text"], line.get("voice", cfg["voice"]))
    lang = "en-gb" if voice.startswith("b") else "en-us"
    samples, sr = k.create(text, voice=voice, speed=cfg.get("speed", 1.0), lang=lang)
    pad = np.zeros(int(sr * 0.12), dtype=samples.dtype)
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        sf.write(tmp.name, np.concatenate([pad, samples, pad]), sr)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp.name, "-codec:a", "libmp3lame", "-q:a", "4",
                        str(out / f"{key}.mp3")], check=True)
    print(f"{key:12s} {len(samples)/sr:4.1f}s  {text}")
