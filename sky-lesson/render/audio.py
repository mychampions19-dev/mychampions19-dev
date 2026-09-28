"""Offline soundtrack for the sky lesson.

Reads out/timeline.json (dumped from index.html by `node render.mjs timeline`) and writes:
  out/music_fx.wav  music + ambience + SFX (the M&E mix)
  out/vo.wav        scratch voiceover, each line fitted to its caption window
  out/mix.wav       final mix, music ducked under the voice
  out/captions.srt  captions matching the burned-in caption bar

The voiceover is a timing guide made with espeak-ng + MBROLA. To swap in a real read,
drop one WAV per line into vo/line_1.wav ... vo/line_7.wav and re-run; those files win.
"""
import json
import os
import subprocess
import tempfile
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
SR = 48000
FFMPEG = os.environ.get("FFMPEG", "ffmpeg")
VOICE = os.environ.get("VO_VOICE", "mb-en1")

tl = json.load(open(os.path.join(OUT, "timeline.json")))
DUR = tl["duration"]
N = int(DUR * SR)
rng = np.random.default_rng(7)


def t_axis(d):
    return np.arange(int(d * SR)) / SR


def add(buf, start, sig):
    i = int(start * SR)
    if i >= len(buf):
        return
    sig = sig[: len(buf) - i]
    buf[i : i + len(sig)] += sig


def decay(d, dec, att=0.005):
    t = t_axis(d)
    return np.minimum(t / att, 1.0) * np.exp(-t / (dec / 5.0))


def tone(f, d, dec, att=0.005, f1=None, shape="sine"):
    t = t_axis(d)
    if f1:
        k = np.log(f1 / f) / d
        ph = 2 * np.pi * f * (np.exp(k * t) - 1) / k
    else:
        ph = 2 * np.pi * f * t
    if shape == "sine":
        w = np.sin(ph)
    elif shape == "triangle":
        w = 2 / np.pi * np.arcsin(np.sin(ph))
    else:
        w = np.sign(np.sin(ph))
    return w * decay(d, dec, att)


def lowpass(x, fc):
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def filt_noise(d, f0, f1, kind):
    """Noise through a swept one-pole filter, done blockwise for speed."""
    n = rng.uniform(-1, 1, int(d * SR))
    out = np.zeros_like(n)
    blocks = 32
    edges = np.linspace(0, len(n), blocks + 1).astype(int)
    lp_state = 0.0
    for b in range(blocks):
        fc = f0 * (f1 / f0) ** (b / blocks)
        a = np.exp(-2 * np.pi * fc / SR)
        seg = n[edges[b] : edges[b + 1]]
        lp = np.empty_like(seg)
        for i, v in enumerate(seg):
            lp_state = (1 - a) * v + a * lp_state
            lp[i] = lp_state
        if kind == "low":
            out[edges[b] : edges[b + 1]] = lp
        elif kind == "high":
            out[edges[b] : edges[b + 1]] = seg - lp
        else:  # band: high-pass the low-passed noise one octave down
            out[edges[b] : edges[b + 1]] = lp - np.convolve(lp, np.ones(int(SR / fc * 2)) / int(SR / fc * 2), "same")
    env = np.interp(t_axis(d), [0, d * 0.3, d], [0, 1, 0])
    return out / (np.max(np.abs(out)) + 1e-9) * env


def mtof(m):
    return 440 * 2 ** ((m - 69) / 12)


# ---------------------------------------------------------------- music
music = np.zeros(N)
for n in tl["music"]:
    f, v = mtof(n["midi"]), n["vel"]
    if n["inst"] == "marimba":
        s = 0.22 * v * tone(f, 0.9, 0.55)
        s[: int(0.3 * SR)] += 0.05 * v * tone(f * 4, 0.3, 0.12)
    elif n["inst"] == "bass":
        s = 0.25 * v * tone(f, 1.6, 1.3, 0.01, shape="triangle")
    else:  # pad: detuned saws, soft attack, low-passed
        d = n["dur"] + 0.6
        t = t_axis(d)
        saw = sum(2 * ((f * 2 ** (c / 1200) * t) % 1) - 1 for c in (-6, 6)) / 2
        env = np.interp(t, [0, 0.5, n["dur"] - 0.3, d], [0, 1, 1, 0])
        s = 0.07 * v * lowpass(saw, 900) * env
    add(music, n["t"], s)

# ---------------------------------------------------------------- ambience
wind = lowpass(rng.uniform(-1, 1, N), 420)
wind /= np.max(np.abs(wind))
wk = np.array(tl["wind"])
wind *= 0.05 * np.interp(np.arange(N) / SR, wk[:, 0], wk[:, 1])

# ---------------------------------------------------------------- SFX
fx = np.zeros(N)
for e in tl["sfx"]:
    g, ty, t0 = e["gain"], e["type"], e["t"]
    if ty == "slide":
        s = 0.16 * filt_noise(0.38, 2400, 500, "low")
    elif ty == "pop":
        s = 0.22 * tone(900, 0.12, 0.09, 0.002, f1=300)
    elif ty == "tok":
        s = 0.3 * tone(320, 0.15, 0.12, 0.002, f1=180)
    elif ty == "tick":
        s = 0.03 * tone(2400, 0.05, 0.03, 0.001, shape="square")
    elif ty == "ping":
        s = 0.07 * tone(1800 + rng.uniform() * 900, 0.3, 0.25)
    elif ty == "pings":
        s = np.zeros(int(1.0 * SR))
        for i in range(10):
            p = 0.07 * tone(1500 + i * 140, 0.4, 0.35)
            s[int(i * 0.05 * SR) : int(i * 0.05 * SR) + len(p)] += p
    elif ty == "chime":
        s = sum(0.12 / (i + 1) * tone(880 * r, 2.0, 1.8) for i, r in enumerate((1, 2.76, 5.4)))
    elif ty == "end":
        s = np.zeros(int(3 * SR))
        for i, f in enumerate((523.25, 659.25, 783.99, 1046.5)):
            p = 0.1 * tone(f, 2.5, 2.4)
            s[int(i * 0.06 * SR) : int(i * 0.06 * SR) + len(p)] += p
    elif ty == "thwip":
        s = 0.15 * tone(300, 0.2, 0.18, 0.005, f1=1400)
    elif ty == "hum":
        s = 0.22 * tone(110, 1.2, 1.1, 0.08, shape="triangle")
    elif ty == "trill":
        s = np.zeros(int(0.7 * SR))
        for i in range(8):
            p = 0.06 * tone(1500 if i % 2 else 1200, 0.1, 0.09)
            s[int(i * 0.07 * SR) : int(i * 0.07 * SR) + len(p)] += p
    elif ty == "whoosh":
        s = 0.2 * filt_noise(1.1, 300, 3000, "band")
    elif ty == "longwhoosh":
        s = 0.16 * filt_noise(3.1, 2600, 400, "band")
    elif ty == "peel":
        s = 0.18 * filt_noise(0.12, 3000, 5000, "high")
    else:
        continue
    add(fx, t0, g * s)


# ---------------------------------------------------------------- voiceover
def read_wav(path):
    with wave.open(path) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
        return a if w.getnchannels() == 1 else a.reshape(-1, w.getnchannels()).mean(1)


def to48k(src, dst, tempo=1.0):
    af = f"atempo={tempo:.4f}," if abs(tempo - 1) > 0.01 else ""
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", src, "-af", f"{af}aresample={SR}", "-ac", "1", "-sample_fmt", "s16", dst], check=True)


def trim(a, thr=0.01):
    idx = np.where(np.abs(a) > thr)[0]
    return a[idx[0] : idx[-1] + 1] if len(idx) else a


vo = np.zeros(N)
report = []


def place(src, t0, window, tag):
    base = src + ".48k.wav"
    to48k(src, base)
    natural = len(trim(read_wav(base))) / SR
    # Fit into the caption window: speed up if long; never slow below 0.92x.
    tempo = min(max(natural / window, 0.92), 1.6)
    fit = src + ".fit.wav"
    to48k(base, fit, tempo)
    a = trim(read_wav(fit))
    a = a / (np.max(np.abs(a)) + 1e-9) * 0.8
    add(vo, t0, a)
    report.append(f"{tag}: {natural:.2f}s -> {len(a) / SR:.2f}s in a {window:.2f}s window")


with tempfile.TemporaryDirectory() as tmp:
    for i, line in enumerate(tl["vo"], 1):
        user = os.path.join(HERE, "vo", f"line_{i}.wav")
        if os.path.exists(user):  # a real recording: one file per line, placed at the line cue
            dst = os.path.join(tmp, f"user{i}.wav")
            subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", user, dst], check=True)
            place(dst, line["t"], line["dur"], f"line {i} (recorded)")
            continue
        # scratch: one phrase per caption chunk, so the voice lands exactly on its caption
        for j, cap in enumerate(c for c in tl["captions"] if c["line"] == i - 1):
            raw = os.path.join(tmp, f"raw{i}_{j}.wav")
            text = cap["text"].replace("—", ",")
            subprocess.run(["espeak-ng", "-v", VOICE, "-s", "128", "-p", "45", "-w", raw, text], check=True, capture_output=True)
            place(raw, cap["start"], cap["end"] - cap["start"] + 0.3, f"line {i}.{j + 1} (scratch)")

# ---------------------------------------------------------------- mix
me = music + wind + fx
# Duck the music bed ~6 dB under the voice (smoothed envelope).
venv = np.convolve(np.abs(vo), np.ones(SR // 10) / (SR // 10), "same")
duck = 1 - 0.5 * np.clip(venv / 0.05, 0, 1)
duck = np.convolve(duck, np.ones(SR // 5) / (SR // 5), "same")
final = music * duck + wind + fx + vo * 0.9
fade = np.interp(np.arange(N) / SR, [0, DUR - 1.0, DUR], [1, 1, 0])


def write(path, x):
    x = x * fade
    x = x / max(1.0, np.max(np.abs(x)) / 0.95)
    st = np.repeat((x * 32767).astype(np.int16)[:, None], 2, axis=1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(st.tobytes())


write(os.path.join(OUT, "music_fx.wav"), me)
write(os.path.join(OUT, "vo.wav"), vo)
write(os.path.join(OUT, "mix.wav"), final)


def ts(s):
    ms = int(round(s * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


with open(os.path.join(OUT, "captions.srt"), "w") as f:
    for i, c in enumerate(tl["captions"], 1):
        f.write(f"{i}\n{ts(c['start'])} --> {ts(c['end'] + 0.35)}\n{c['text']}\n\n")

print("\n".join(report))
print("wrote music_fx.wav, vo.wav, mix.wav, captions.srt")
