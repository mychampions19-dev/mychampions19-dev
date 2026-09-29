"""Approximate word-level alignment of a TTS read to its script, with no ASR.
Detects pauses with ffmpeg, maps them onto word boundaries (preferring punctuation) with a
monotonic DP, then spreads words inside each speech run by syllable weight.
Usage: python3 align.py audio.mp3 script.txt > words.tsv   (start, end, word)"""
import re, subprocess, sys

FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
NUM = {"30": "thirty", "45": "forty five", "14": "fourteen", "2025": "twenty twenty five", "60": "sixty", "90": "ninety",
       "10": "ten", "15": "fifteen", "16": "sixteen", "20": "twenty", "24": "twenty four", "7": "seven", "8": "eight",
       "9": "nine", "11": "eleven", "3": "three", "1": "one", "2": "two", "5": "five", "4": "four", "6": "six", "12": "twelve"}


def syl(w):
    w = w.lower()
    parts = re.split(r"[:.]", w) if re.search(r"\d", w) else [w]
    if re.search(r"\d", w):
        w = " ".join(NUM.get(p, p) for p in parts if p)
    n = sum(max(1, len(re.findall(r"[aeiouy]+", x)) - (1 if x.endswith("e") and len(x) > 3 and not x.endswith("le") else 0))
            for x in w.split())
    return max(1, n)


def pauses(audio, db=-35, d=0.12):
    out = subprocess.run([FF, "-hide_banner", "-i", audio, "-af", f"silencedetect=n={db}dB:d={d}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    s = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    e = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    dur = float(re.search(r"Duration: (\d+):(\d+):([\d.]+)", out).groups()[2]) + 60 * int(re.search(r"Duration: (\d+):(\d+)", out).group(2))
    return list(zip(s, e)), dur


def align(audio, text):
    words = re.findall(r"[\w'’:.\-]+[—,.;:?!]*|—", text.replace("—", " — "))
    words = [w for w in words if w != "—"]
    toks = [re.sub(r"[—,.;:?!]+$", "", w) for w in words]
    punct = [1.0 if re.search(r"[.?!]$", w) else .6 if re.search(r"[,;:]$", w) else .45 if w.endswith("—") else 0 for w in words]
    # a dash in the source text sits between words, flag the word before it
    raw = text.replace("—", " — ").split()
    k = -1
    for r in raw:
        if r == "—" and k >= 0: punct[k] = max(punct[k], .45)
        elif r != "—": k += 1
    wt = [syl(t) + .35 for t in toks]
    P, dur = pauses(audio)
    lead = P[0][1] if P and P[0][0] < .05 else 0.0
    P = [p for p in P if p[0] > .05 and p[1] < dur - .05]
    speech_total = dur - lead - sum(e - s for s, e in P)
    rate = speech_total / sum(wt)
    import math
    n, m = len(words), len(P)
    def pen(b):
        return 0 if punct[b] >= .6 else 1.0 if punct[b] else 7
    def segcost(t0, t1, b0, b):
        W = sum(wt[b0 + 1:b + 1])
        d = max(t1 - t0, .05)
        return 10 * math.log(d / (W * rate)) ** 2
    # state: (j, b) = pause j sits after word b. start state (-1, -1) at time `lead`
    INF = 1e18
    best = {(-1, -1): 0.0}; back = {}
    for j in range(m):
        for b in range(n - 1):
            bv = INF; bk = None
            for (j0, b0), v0 in list(best.items()):
                if j0 >= j or b0 >= b or j0 < j - 3 or b - b0 > 45: continue
                t0 = lead if j0 < 0 else P[j0][1]
                v = v0 + segcost(t0, P[j][0], b0, b) + pen(b) + 3 * (j - j0 - 1)
                if v < bv: bv, bk = v, (j0, b0)
            if bk: best[(j, b)] = bv; back[(j, b)] = bk
    # finish: last segment runs to the end of the audio
    fin = None; fv = INF
    for (j0, b0), v0 in best.items():
        if n - 1 - b0 > 45 or j0 < m - 4: continue
        t0 = lead if j0 < 0 else P[j0][1]
        v = v0 + segcost(t0, dur, b0, n - 1) + 3 * (m - 1 - j0)
        if v < fv: fv, fin = v, (j0, b0)
    amap = {}; st = fin
    while st and st[0] >= 0:
        amap[st[1]] = P[st[0]]; st = back.get(st)
    # lay out words: runs between mapped pauses
    res = []; t = lead; start = 0
    bounds = sorted(amap) + [n - 1]
    for b in bounds:
        run = range(start, b + 1)
        end_t = amap[b][0] if b in amap else dur
        W = sum(wt[k] for k in run) or 1
        for k in run:
            d = (end_t - t) * wt[k] / W
            res.append((t, t + d, toks[k])); t += d
        t = amap[b][1] if b in amap else t
        start = b + 1
    return res


if __name__ == "__main__":
    for s, e, w in align(sys.argv[1], open(sys.argv[2]).read()):
        print(f"{s:.2f}\t{e:.2f}\t{w}")
