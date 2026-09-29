"""Procedural one-shots for the series (fixed seeds, so every episode gets identical sounds).

    python3 sfx_synth.py            # writes sfx/step_*.wav, sfx/touch_ice.wav, sfx/crackle_*.wav, sfx/roomtone.wav
"""
import os
import wave

import numpy as np

SR = 48000
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sfx")


def save(name, x):
    x = x / (np.abs(x).max() + 1e-9) * 0.9
    with wave.open(os.path.join(OUT, name), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def bandpass(x, lo, hi):
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X = np.fft.rfft(x)
    X *= 1 / (1 + (lo / np.maximum(f, 1)) ** 4) / (1 + (f / hi) ** 4)
    return np.fft.irfft(X, len(x))


def step(seed):
    """Tiny soft footfall on a slightly wet wooden table."""
    r = np.random.default_rng(seed)
    n = int(0.09 * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * r.uniform(420, 520) * t) * np.exp(-t / 0.012)
    tap = bandpass(r.standard_normal(n), 1800, 6000) * np.exp(-t / 0.004)
    wet = bandpass(r.standard_normal(n), 2500, 9000) * np.exp(-((t - 0.012) / 0.01) ** 2) * 0.25
    return 0.6 * body + tap + wet


def touch_ice():
    """Fingertip pressing a cold wet ice cube: small squeak plus a few crackles."""
    r = np.random.default_rng(11)
    n = int(0.6 * SR)
    t = np.arange(n) / SR
    f = 1500 + 900 * np.clip(t / 0.12, 0, 1)
    squeak = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-((t - 0.07) / 0.05) ** 2)
    squeak *= 1 + 0.3 * np.sin(2 * np.pi * 38 * t)
    crack = np.zeros(n)
    for c in r.uniform(0.08, 0.5, 6):
        i = int(c * SR)
        m = min(n - i, 300)
        crack[i:i + m] += r.standard_normal(m) * np.exp(-np.arange(m) / 40) * r.uniform(0.3, 1)
    return 0.5 * squeak + bandpass(crack, 3000, 12000)


def crackle(seed):
    """One tiny ice micro-crack / fizz tick."""
    r = np.random.default_rng(seed)
    n = int(0.03 * SR)
    x = r.standard_normal(n) * np.exp(-np.arange(n) / r.uniform(25, 90))
    return bandpass(x, 3500, 14000)


def roomtone(seconds=12.0):
    """Very soft pink-ish air, seamless loop."""
    r = np.random.default_rng(5)
    n = int(seconds * SR)
    X = np.fft.rfft(r.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR)
    X /= np.sqrt(np.maximum(f, 20))
    X *= 1 / (1 + (f / 3000) ** 2)
    return np.fft.irfft(X, n)  # FFT-generated noise loops seamlessly


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i in range(6):
        save(f"step_{i}.wav", step(100 + i))
    save("touch_ice.wav", touch_ice())
    for i in range(8):
        save(f"crackle_{i}.wav", crackle(200 + i))
    save("roomtone.wav", roomtone())
    print("ok")
