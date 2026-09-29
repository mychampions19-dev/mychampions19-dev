# Tiny Monkey Science: series style

Every episode follows these rules so the series looks and sounds like one production.

## Picture
- Keep the source framing: no zooms, crops, reframes or camera moves, and no text, captions or graphics.
- Output 1920×1080, 24 fps. Scale any 720p clip up with Lanczos.
- Joins are 12-frame (0.5 s) dissolves, used as time-lapse dissolves. Use a hard cut when a dissolve would ghost badly.
- Start with a 0.4 s fade in from black and end with a 1.0 s fade out. There is no title card.
- Before editing, check every clip frame by frame for AI glitches (for example, water appearing from nowhere). Cut them out instead of hiding them.
- A short shot may be slowed to no less than 0.75×, using motion-compensated interpolation (`minterpolate mi_mode=mci`). Check the character frame by frame afterwards.

## Narration
- Voice: ElevenLabs **Ben – Explanation videos and audiobooks** (`BhFRJzCXkJugxsZIDyx8`), model `eleven_multilingual_v2`.
- Generate one take per episode, then cut it into phrases and place each phrase against the picture in `cues.json`.
- Leave about 0.5–0.8 s between phrases, and about 1.5 s before a new idea or the closing line.
- Start the first line at about 0.7 s. Leave at least 1 s after the last word before the video ends.

## Music: series theme (`score.py`)
- Always the same theme: C major, 80 BPM, rendered with FluidSynth + FluidR3_GM.
- Instruments are GM Acoustic Piano, Celesta, Pizzicato Strings and Slow Strings.
- Layers enter at the picture cuts (`sections`): piano → + celesta → + pizzicato → + string pad. It ends on a held C(add9) chord that fades with the picture.
- Change only the duration and the section times, never the notes, instruments or tempo.

## Sound effects (`sfx/`)
| Kind | Files | Use |
|---|---|---|
| `drip_hero` | `drip_hero.wav` (ElevenLabs) | The one drop the narration points out, synced to the splash frame |
| `drip` | `drip_a`–`drip_f.wav` (ElevenLabs) | Sparse drips once the ice is melting, taken from on-screen drips and the clips' own audio |
| `step` | `step_0`–`step_5.wav` (synthesized) | The monkey's tiny footsteps; alternate files and trims |
| `touch` | `touch_ice.wav` (synthesized) | The monkey's hand on the ice |
| `crackle` | `crackle_0`–`crackle_7.wav` (synthesized) | Very faint melting texture, about 1 per second |
| room tone | `roomtone.wav` (synthesized) | Always on, very quiet, so the joins never drop to dead silence |

To recreate the synthesized sounds, run `python3 sfx_synth.py` (fixed seeds, so the output is identical every time).
The clips' own audio (birds, drips) stays in as ambience, crossfaded at each join, with any built-in voices or "ooh" sounds turned down.

## Mix (`build_audio.py`, fixed levels)
- The finished mix is about −16 LUFS, with peaks limited to −1 dBFS.
- Voice sits on top. Music and ambience are about 16 dB under the voice in pauses, and dip another 6 dB while the voice is speaking.
- Effects are placed individually per episode in `cues.json`. Per-cue trims stay within ±6 dB.

## Making a new episode
1. Put the clips in order, cut out glitches, and render the picture with the dissolves above.
2. Generate the voiceover with Ben. Find the phrase boundaries (silence detection) and place each phrase against the picture.
3. Render the clips' own audio with the same crossfades into `native_clips.wav`.
4. Write `cues.json` (copy `../why-ice-melts/cues.json` as the template).
5. Run `python3 series-kit/build_audio.py <episode>/cues.json mix.wav`, then combine it with the picture.
