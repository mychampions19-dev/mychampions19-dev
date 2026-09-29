"""Render clips → mix SFX → mux final MP4s.
Usage: python3 build.py S01-B02 [S01-B04 ...]   (clip ids; names come from CLIPS below)"""
import json, subprocess, sys
from pathlib import Path
import sfx

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "03_graphics"
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"

# clip id -> (section folder, final file name)
CLIPS = {
    "S01-B02": ("S01_MetabolicSwitch", "S01-B02_MG_9AMSwitch_v1"),
    "S01-B04": ("S01_MetabolicSwitch", "S01-B04_MG_ZeroCalories_v1"),
    "S01-B06": ("S01_MetabolicSwitch", "S01-B06_MG_BurnVsStore_v1"),
    "S01-B07": ("S01_MetabolicSwitch", "S01-B07_MG_7MistakesPreview_v1"),
}


def build(cid):
    folder, name = CLIPS[cid]
    tmp = ROOT / "tmp"; tmp.mkdir(exist_ok=True)
    base = tmp / name
    subprocess.run(["node", str(ROOT / "render.js"), str(ROOT / "clips" / f"{cid}.html"), str(base)], check=True)
    meta = json.loads((base.with_suffix(".sfx.json")).read_text())
    events = [(t, getattr(sfx, kind)(**(kw or {}))) for t, kind, *rest in meta["sfx"] for kw in [rest[0] if rest else None]]
    wav = base.with_suffix(".wav")
    sfx.write_wav(wav, sfx.mix(events, meta["duration"]))
    dest = OUT / folder; dest.mkdir(parents=True, exist_ok=True)
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", str(base) + ".video.mp4", "-i", str(wav),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                    str(dest / f"{name}.mp4")], check=True)
    print("→", dest / f"{name}.mp4")


if __name__ == "__main__":
    for c in sys.argv[1:] or CLIPS:
        build(c)
