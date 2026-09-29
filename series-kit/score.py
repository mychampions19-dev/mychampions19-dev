"""Series theme: gentle felt-piano underscore, rendered from MIDI with FluidSynth.

The same motif, key, tempo and instrument palette is used in every episode so the
series sounds consistent. Only the length and the section markers change.

    python3 score.py --duration 26.92 --sections 5.5,11,16.5,22 --out music.wav

Sections (the picture cut points) control when layers enter:
  section 1: piano alone
  section 2: + celesta sparkle
  section 3: + pizzicato strings
  section 4: + warm string pad
  last:      everything resolves to a held tonic chord that fades out at the end.
"""
import argparse
import subprocess
import tempfile

import mido

SOUNDFONT = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
BPM = 80
TPB = 480  # ticks per beat
KEY_SHIFT = 0  # keep 0 for series consistency (C major)

# GM programs
PIANO, CELESTA, PIZZ, STRINGS = 0, 8, 45, 49

# Four-bar loop plus a turnaround, each bar = 4 beats. (root, chord tones above)
PROGRESSION = [
    (48, [64, 67, 71, 74]),  # Cmaj9
    (45, [60, 64, 67, 71]),  # Am9-ish
    (41, [57, 60, 64, 67]),  # Fmaj9
    (43, [59, 62, 67, 69]),  # G6/9
    (40, [59, 64, 67, 71]),  # Cmaj7/E
    (41, [57, 60, 64, 69]),  # Fmaj7
    (38, [57, 60, 65, 69]),  # Dm7
    (43, [60, 62, 65, 67]),  # G7sus4
]
TONIC = (36, [55, 60, 64, 67, 74])  # C add9, final held chord

CELESTA_MOTIF = [(0.5, 79), (1.0, 76), (1.5, 74), (2.5, 76)]  # beat offset, note


def build(duration, sections, path):
    beat = 60.0 / BPM
    bar = 4 * beat
    events = []  # (time_s, channel, type, note, vel)

    def note(t, ch, n, vel, length):
        if t >= duration - 0.05:
            return
        end = min(t + length, duration + 1.5)
        events.append((t, ch, "on", n + KEY_SHIFT, vel))
        events.append((end, ch, "off", n + KEY_SHIFT, 0))

    marks = [0.0] + list(sections) + [duration]
    final_start = marks[-2]
    n_bars = int(final_start // bar)
    t0 = 0.35  # tiny breath before the first note

    for b in range(n_bars + 1):
        t = t0 + b * bar
        if t >= final_start - 0.2:
            break
        root, tones = PROGRESSION[b % len(PROGRESSION)]
        layer = sum(1 for m in marks[1:-1] if t >= m - 0.01)  # 0..n sections passed
        # piano: soft bass + broken chord
        note(t, 0, root, 42, bar * 1.1)
        note(t + 0.02, 0, root + 12, 30, bar * 0.9)
        for i, (off, idx) in enumerate([(0.5, 0), (1.0, 1), (1.5, 2), (2.5, 3), (3.0, 1)]):
            note(t + off * beat, 0, tones[idx], 38 if i else 44, beat * 2.2)
        if layer >= 1 and b % 2 == 1:
            for off, n in CELESTA_MOTIF:
                note(t + off * beat, 1, n, 34, beat * 1.2)
        if layer >= 2:
            for off in (0.0, 2.0):
                note(t + off * beat, 2, root + 12, 40, beat * 0.5)
                note(t + (off + 1) * beat, 2, tones[0], 34, beat * 0.5)
        if layer >= 3:
            for n in tones[:3]:
                note(t, 3, n - 12, 30, bar * 1.02)

    # resolve: held tonic from the last section to the end
    tr = max(final_start + 0.3, t0)
    root, tones = TONIC
    note(tr, 0, root, 44, duration - tr + 1.5)
    for i, n in enumerate(tones):
        note(tr + 0.12 * i, 0, n, 36, duration - tr + 1.5)
    for n in tones[:3]:
        note(tr, 3, n, 26, duration - tr + 1.5)
    note(tr + 0.9, 1, 84, 28, 2.0)

    mid = mido.MidiFile(ticks_per_beat=TPB)
    tr_ = mido.MidiTrack()
    mid.tracks.append(tr_)
    tr_.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(BPM)))
    for ch, prog in enumerate([PIANO, CELESTA, PIZZ, STRINGS]):
        tr_.append(mido.Message("program_change", channel=ch, program=prog, time=0))
        tr_.append(mido.Message("control_change", channel=ch, control=91, value=70, time=0))  # reverb send
        tr_.append(mido.Message("control_change", channel=ch, control=93, value=10, time=0))  # chorus send
    tr_.append(mido.Message("control_change", channel=3, control=7, value=80, time=0))
    tr_.append(mido.Message("control_change", channel=1, control=7, value=85, time=0))
    tr_.append(mido.Message("control_change", channel=0, control=64, value=0, time=0))

    events.sort(key=lambda e: (e[0], e[2] == "on"))
    last = 0
    for t, ch, kind, n, vel in events:
        ticks = int(round(mido.second2tick(t, TPB, mido.bpm2tempo(BPM))))
        delta, last = ticks - last, ticks
        msg = "note_on" if kind == "on" else "note_off"
        tr_.append(mido.Message(msg, channel=ch, note=n, velocity=vel, time=max(0, delta)))
    mid.save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duration", type=float, required=True)
    ap.add_argument("--sections", required=True, help="comma-separated cut times in seconds")
    ap.add_argument("--out", default="music.wav")
    a = ap.parse_args()
    sections = [float(s) for s in a.sections.split(",") if s]
    with tempfile.TemporaryDirectory() as d:
        midi, raw = f"{d}/theme.mid", f"{d}/raw.wav"
        build(a.duration, sections, midi)
        subprocess.run(["fluidsynth", "-ni", "-g", "0.6", "-r", "48000", "-F", raw, SOUNDFONT, midi],
                       check=True, capture_output=True)
        fade_st = max(0, a.duration - 2.0)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af",
                        f"highpass=f=60,lowpass=f=7000,atrim=0:{a.duration},"
                        f"afade=t=out:st={fade_st}:d=2.0,loudnorm=I=-20:TP=-2:LRA=11:linear=true",
                        "-ar", "48000", a.out], check=True)


if __name__ == "__main__":
    main()
