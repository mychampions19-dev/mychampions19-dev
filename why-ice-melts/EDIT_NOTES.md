# Why Ice Melts: edit notes

Output: `why_ice_melts_final.mp4`, 1920×1080, 24 fps, 26.9 s, AAC 48 kHz, about −16 LUFS.

## Sequence (filename order, which also matches how far the ice has melted)

| # | Source | Used | Timeline | Picture |
|---|--------|------|----------|---------|
| 1 | Monkey1 | 0.0–6.0 s (upscaled from 720p, Lanczos) | 0.0–6.0 | Intact cube, monkey inspecting with magnifier |
| 2 | Monkey_2 | full | 5.5–11.5 | First drip falls and splashes; monkey reacts |
| 3 | Monkey_3 | full | 11.0–17.0 | Monkey touches the wet cube |
| 4 | Monkey_4 | full | 16.5–22.5 | Smaller cube, puddle; monkey walks round and sits |
| 5 | Monkey_5 | 2.08–6.0 s, slowed to 0.78× (motion-interpolated) | 22.0–26.9 | Monkey ponders beside the puddle |

Transitions: 12-frame (0.5 s) dissolves, used as time-lapse dissolves (each cut jumps forward in how far the ice has melted).
There is a 0.4 s fade in from black at the start and a 1 s fade out at the end. There are no zooms, crops, reframes, text or grading.
Exposure and colour already match at every cut (average brightness within about 1%).

### Fixes
- **Clip 5, 1.17–2.05 s:** a thin stream of water pours onto the cube from above the frame (an AI glitch, and misleading science). It has been cut out.
- **Clip 5 length:** after that cut, only 3.9 s was left. It is slowed to 0.78× with motion interpolation (checked frame by frame on the monkey, with no ghosting) so the last line has room to finish.
- **Clip 2, about 3.2–4.9 s:** the built-in "ooh" sound effect is turned down so it doesn't clash with the narration.

## Voiceover (drafted, because no script was attached)
Voice: ElevenLabs "Ben", a calm British male voice (eleven_multilingual_v2). Each phrase is placed by hand against the picture:

| Time | Line | Picture at that moment |
|------|------|------|
| 0.7 | "Here's an ice cube. It looks solid… and perfectly still." | Intact cube |
| 5.6 | "But look closely." | Dissolve into the dripping cube |
| 6.9 | "A drop of water." | Drop falls and splashes (about 7.0–7.5 s) |
| 8.3 | "It's starting to melt." | Monkey reacts |
| 9.9 | "Ice is simply water that has frozen." | Carries across into clip 3 |
| 12.5 | "Its tiny particles are locked tightly together." | Monkey's hand on the ice |
| 15.3 | "Warm air in the kitchen passes heat into the ice." | Carries across into clip 4 |
| 18.3 | "The particles start to wiggle, break free… and flow away as water." | Puddle spreading, drips |
| 22.9 | "So ice melts because it's soaking up heat from the world around it." | Clip 5, ending |

## Audio (v2: produced music and sound effects, built with `../series-kit/`)
- **Music:** the series theme from `score.py`, played on sampled piano, celesta, pizzicato strings and a string pad (FluidSynth, FluidR3_GM).
  A new layer enters at each cut (5.5 / 11 / 16.5 / 22 s), and it ends on a held chord that fades with the picture.
- **Sound effects (58 cues in `cues.json`):**
  - splash drop at 7.47 s, synced to the frame where the splash lands
  - 11 sparse drips from clip 2 onward
  - 16 tiny footsteps (clip 1 walk, clip 3 step back, clip 4 walk and sit, clip 5 crouch)
  - two touches on the ice (11.3 s and 13.9 s)
  - faint melting crackle throughout
  - an always-on room tone
- **Ambience:** the clips' own birdsong and drips, crossfaded at each join, with the clip 2 "ooh" turned down.
- **Mix:** −15.6 LUFS, −1 dBFS peak. The background sits about 16 dB under the narration in pauses and dips 6 dB further under the voice.
- To rebuild: `python3 ../series-kit/build_audio.py cues.json mix.wav`, then combine it with the picture.

## Transitions to watch
The monkey never lands in the same place from one clip to the next, so each dissolve briefly shows two faint monkeys.
That reads as a normal "time passing" dissolve, and I think it's the right choice. If you'd rather avoid it, the simplest option is:
- **Hard cuts instead of dissolves.** Each cut then reads as "a little later". This works best at 1→2 and 3→4, where the ice clearly changes.
- **Clip 4 → 5** is the weakest join, because both clips were generated from the same starting frame (the monkey goes from sitting to standing).
  A straight cut there on the line "So ice melts…" would also work.
  The cleanest fix is to regenerate clip 5 starting from clip 4's last frame (monkey sitting), not to add any effect.
