"""Synthesised sound-effect library for the motion graphics (no licensing issues).
Each function returns a mono float32 numpy array at SR. mix() places them on a timeline."""
import numpy as np, wave

SR = 48000
rng = np.random.default_rng(7)


def _env(n, a=0.005, r=0.1):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4))
    rel = np.clip((t[-1] - t) / max(r, 1e-4), 0, 1)
    return e * rel


def _lp(x, k):
    """Cheap one-pole low-pass, k in (0,1]; smaller = darker. k may be an array."""
    y = np.empty_like(x)
    k = np.broadcast_to(k, x.shape)
    acc = 0.0
    for i in range(len(x)):
        acc += k[i] * (x[i] - acc)
        y[i] = acc
    return y


def whoosh(dur=0.6, rise=True, vol=0.5):
    n = int(dur * SR)
    t = np.linspace(0, 1, n)
    noise = rng.standard_normal(n)
    shape = np.sin(np.pi * t) ** 2
    k = 0.02 + 0.25 * (t if rise else 1 - t)
    return (_lp(noise, k) * shape * vol * 3).astype(np.float32)


def pop(freq=700, dur=0.12, vol=0.45):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = freq * (1 + 1.5 * np.exp(-t * 60))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * np.exp(-t * 28) * vol).astype(np.float32)


def click(vol=0.6):
    n = int(0.05 * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 90)
    snap = rng.standard_normal(n) * np.exp(-t * 400)
    return ((body * 0.8 + snap * 0.5) * vol).astype(np.float32)


def clunk(vol=0.8):
    """Heavy lever switch."""
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    thud = np.sin(2 * np.pi * 70 * t) * np.exp(-t * 18)
    metal = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, d in [(820, 30), (1330, 40), (2100, 55)])
    snap = rng.standard_normal(n) * np.exp(-t * 250)
    return ((thud * 1.0 + metal * 0.18 + snap * 0.4) * vol).astype(np.float32)


def tick(vol=0.35):
    n = int(0.03 * SR)
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 300) * vol).astype(np.float32)


def ding(freq=1320, dur=1.2, vol=0.35):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * freq * m * t) * np.exp(-t * d) for m, a, d in [(1, 1, 3), (2.01, .4, 5), (3.02, .2, 8)])
    return (s * vol * _env(n, 0.002, 0.3)).astype(np.float32)


def buzz(dur=0.35, vol=0.3):
    """'Wrong' buzzer."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sign(np.sin(2 * np.pi * 110 * t)) * 0.6 + np.sin(2 * np.pi * 116 * t) * 0.4
    return (_lp(s, 0.15) * _env(n, 0.005, 0.08) * vol).astype(np.float32)


def riser(dur=1.5, vol=0.25):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 200 * (2 ** (t / dur * 2.5))
    ph = 2 * np.pi * np.cumsum(f) / SR
    tone = np.sin(ph) * 0.5 + np.sin(ph * 1.5) * 0.25
    noise = _lp(rng.standard_normal(n), 0.05 + 0.3 * t / dur)
    return ((tone + noise) * (t / dur) ** 2 * vol).astype(np.float32)


def impact(vol=0.9):
    n = int(1.0 * SR)
    t = np.arange(n) / SR
    f = 55 + 90 * np.exp(-t * 12)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4)
    crack = _lp(rng.standard_normal(n), 0.4) * np.exp(-t * 30)
    return ((boom + crack * 0.5) * vol).astype(np.float32)


def sizzle(dur=1.5, vol=0.12):
    n = int(dur * SR)
    noise = rng.standard_normal(n)
    hp = noise - _lp(noise, 0.3)
    crackle = (rng.random(n) > 0.9985) * rng.standard_normal(n) * 4
    return ((hp + crackle) * _env(n, 0.2, 0.4) * vol).astype(np.float32)


def freeze(dur=1.2, vol=0.18):
    """Icy shimmer for the storage side."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t + i) for i, f in enumerate([2637, 3136, 3951, 4699]))
    trem = 0.6 + 0.4 * np.sin(2 * np.pi * 9 * t)
    return (s / 4 * trem * _env(n, 0.3, 0.5) * vol).astype(np.float32)


def mix(events, dur):
    """events: list of (time_sec, sample_array). Returns stereo int16 with a soft limiter."""
    out = np.zeros(int(dur * SR), np.float32)
    for at, s in events:
        i = int(at * SR)
        if i >= len(out):
            continue
        s = s[: len(out) - i]
        out[i : i + len(s)] += s
    out = np.tanh(out * 1.1) * 0.85  # soft limit, leaves headroom under the voice
    st = np.stack([out, out], 1)
    return (st * 32767).astype(np.int16)


def write_wav(path, data):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())
