"""Mix an episode's soundtrack from a cue sheet, using the series' fixed levels.

    python3 build_audio.py ../why-ice-melts/cues.json out_mix.wav

Layers (fixed series levels, in dB relative to full scale peaks):
  voice   loudness-matched so the finished mix lands near -16 LUFS; always on top
  music   series theme (score.py), about 14 dB under the voice, ducked further while he speaks
  native  the clips' own audio (birds, drips), crossfaded at each dissolve
  room    a very soft room-tone loop so the joins never drop to dead silence
  sfx     one-shots placed by hand against the picture
"""
import json
import os
import subprocess
import sys

import numpy as np

SR = 48000
KIT = os.path.dirname(os.path.abspath(__file__))

LEVELS = {  # linear gains applied after each layer is normalised
    "music_lufs": -30.5,
    "room_db": -54.5,
    "sfx_db": {"drip_hero": -17.5, "drip": -25.5, "step": -35.5, "touch": -29.5, "crackle": -44.5},
    "duck_db": -6.0,  # extra reduction of music + native + room under the voice
}


def load(path, ch=1):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", str(ch), "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32).copy()
    return x.reshape(-1, ch) if ch > 1 else x


def lufs(path):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    vals = [l for l in out.splitlines() if l.strip().startswith("I:")]
    return float(vals[-1].split()[1])


def db(x):
    return 10 ** (x / 20)


def place(buf, x, t, gain=1.0):
    i = int(t * SR)
    if i >= len(buf):
        return
    m = min(len(x), len(buf) - i)
    buf[i:i + m] += x[:m] * gain


def main(cue_path, out_path):
    cue = json.load(open(cue_path))
    base = os.path.dirname(os.path.abspath(cue_path))
    T = cue["duration"]
    n = int(T * SR)

    # voice: slice the take into phrases and place each one against the picture
    vo_src = load(os.path.join(base, cue["voice"]["file"]))
    vo = np.zeros(n, np.float32)
    for a, b, at in cue["voice"]["segments"]:
        s = vo_src[int(a * SR):int(b * SR)].copy()
        s[:960] *= np.linspace(0, 1, 960)
        s[-3360:] *= np.linspace(1, 0, 3360)
        place(vo, s, at)
    tmp = out_path + ".vo.wav"
    write(tmp, vo)
    vo *= db(-18.5 - lufs(tmp))
    os.remove(tmp)

    # music
    mpath = out_path + ".music.wav"
    subprocess.run([sys.executable, os.path.join(KIT, "score.py"), "--duration", str(T),
                    "--sections", ",".join(str(s) for s in cue["sections"]), "--out", mpath], check=True)
    music = load(mpath, 2)[:n]
    music = np.pad(music, ((0, n - len(music)), (0, 0)))
    music *= db(LEVELS["music_lufs"] - lufs(mpath))
    os.remove(mpath)

    # native clip audio (already crossfaded by the video step) and room tone
    native = load(os.path.join(base, cue["native"]))[:n]
    native = np.pad(native, (0, n - len(native)))
    room = np.resize(load(os.path.join(KIT, "sfx", "roomtone.wav")), n) * db(LEVELS["room_db"])

    # sfx
    sfx = np.zeros(n, np.float32)
    for c in cue["sfx"]:
        x = load(os.path.join(KIT, "sfx", c["file"]))
        x = x / (np.abs(x).max() + 1e-9)
        gain = db(LEVELS["sfx_db"][c["kind"]] + c.get("trim_db", 0))
        place(sfx, x, c["t"], gain)

    # duck the beds under the voice (smoothed envelope follower)
    env = np.abs(vo)
    win = int(0.05 * SR)
    env = np.convolve(env, np.ones(win) / win, "same")
    on = (env > 0.01).astype(np.float32)
    k = int(0.35 * SR)
    on = np.convolve(on, np.ones(k) / k, "same").clip(0, 1)
    duck = 1 - on * (1 - db(LEVELS["duck_db"]))

    mono = vo + (native + room) * duck + sfx
    mix = music * duck[:, None] + mono[:, None]
    fo = int(cue.get("fade_out", 1.0) * SR)
    mix[-fo:] *= (np.linspace(1, 0, fo) ** 1.5)[:, None]
    fi = int(cue.get("fade_in", 0.4) * SR)
    mix[:fi] *= np.linspace(0, 1, fi)[:, None]
    # true-peak-safe limiter instead of scaling the whole mix down
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                    "-af", "alimiter=limit=0.89:attack=3:release=60:level=false,aresample=48000",
                    "-c:a", "pcm_s16le", out_path], input=mix.astype(np.float32).tobytes(), check=True)
    print(f"mix -> {out_path}  voice/music/native/sfx peaks:",
          *(f"{20*np.log10(np.abs(v).max()+1e-9):.1f}" for v in (vo, music, native, sfx)))


def write(path, x):
    import wave
    with wave.open(path, "wb") as w:
        w.setnchannels(1 if x.ndim == 1 else x.shape[1])
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
