# Why Is the Sky Blue? — Motion Design Package

**Topic:** Rayleigh scattering
**Core idea:** Short light waves bounce off air molecules far more than long ones, so blue light reaches your eyes from every part of the sky.
**Audience:** Curious 10–14 year olds (and anyone who never got a straight answer).
**Runtime:** 86 s · 1920×1080 · 24 fps · captions on

---

## 1. Concept

One ray of sunlight goes on a journey. At the prism it splits into colours, and each colour becomes a wave. It then crosses a crowd of tiny air molecules, and the short blue waves get knocked all over the sky. Pip, a small coral pixel creature, follows the ray the whole way. Nothing changes by cutting. Each scene is the ray changing shape. The sun's glow becomes a beam, the beam becomes waves, the waves meet molecules, the scattered paths become the sky, and at the end the long evening path becomes the recap diagram.

**One cause-and-effect:** *shorter wavelength → more scattering → blue fills the sky (and a longer path strips the blue away at sunset).*

## 2. Visual system

| Element | Treatment |
|---|---|
| Frame | A dark charcoal terminal window (`sky.why — ~/lessons`) with the paper stage inside it |
| Materials | Torn-paper shapes with ragged edges, dry-gouache fills with a speckled grain, crayon hatching, pencil labels |
| Palette | Coral `#E8765A` · Mustard `#E3B23C` · Teal `#3E9C9A` · Cream `#F3EAD8` · Charcoal `#2B2926` (plus a muted violet tint used only once, for the violet note) |
| Colour meaning | Teal = blue light, Coral = red light, Mustard = yellow light / the sun. These stay fixed for the whole film |
| Depth | Soft cardboard shadows (offset 6 px, blur 10 px, 25% charcoal) |
| Boil | Every paper vertex re-jitters by 1–2 px at 8 fps (every 3rd frame). The jitter is seeded, so the result is the same on every render |
| Type | Monospace pencil labels, kept to 1–4 words. Captions sit in the terminal's bottom bar |

## 3. Character sheet — Pip

- A 10×8 coral pixel block with two 1-pixel black eyes, four 1-pixel legs and no mouth. Pip's feelings come from eye shape and hopping.
- Scale: always 12 px per pixel (120×96 px on screen). Pip never changes size. The camera is what moves.
- Poses: `idle` (1 px breathe bob), `look-up` (eyes shift up 1 px), `walk` (legs alternate), `hop` (squash 1 pixel row, then lift), `blink` (eyes go to a 1-pixel line), `wave` (one side pixel lifts).
- Role: a curious guide. Pip points at things, looks at things and reacts. Pip never talks on screen.

## 4. Timestamped storyboard

### SCENE 1 — 0:00–0:09 · Hook
- **Learning purpose:** Raise the puzzle: sunlight is white, yet the sky is blue.
- **Visual:** A cream paper landscape: teal sky card, layered teal-green torn hills, and a mustard sun with pencil rays. Pip stands on the hill. Labels: "sunlight: white?" and later "sky: blue".
- **Motion:** Entrance: the paper layers slide up from below and settle with a slight overshoot. Primary action: Pip walks in, stops and looks up. Secondary reaction: a "?" pops out above Pip. Exit: the camera pushes toward the sun.
- **Voiceover:** "Look up on a clear day. The sky is blue — but sunlight is white. So where does the blue come from?"
- **Sound:** A soft marimba motif starts, with a light wind bed. A paper slide sound as the layers enter, and a pop for the "?".
- **Transition:** The sun's glow narrows into a single white beam that shoots right, and the landscape falls away behind it.

### SCENE 2 — 0:09–0:21 · Familiar world
- **Learning purpose:** Sunlight is a mix of colours, and each colour is a wave with its own wavelength.
- **Visual:** The white beam hits a torn-paper prism and fans into coral, mustard and teal ribbons. The ribbons straighten into three waves: red is long, blue is short. Pencil brackets measure one wavelength on each ("long", "short").
- **Motion:** Entrance: the beam arrives. Primary action: the ribbons fan out, then become waves. Secondary reaction: Pip, bottom-left, looks from one wave to the other. Exit: the waves move right.
- **Voiceover:** "Sunlight is every colour travelling together. Each colour is a wave: red with long, lazy wiggles, blue with short, quick ones."
- **Sound:** A glass chime as the prism splits the light, a low hum for the red wave and a quick high trill for the blue.
- **Transition:** The waves come back together into one white beam, which travels right into a haze of dots.

### SCENE 3 — 0:21–0:31 · Disruption
- **Learning purpose:** Light has to cross the air, and air is made of molecules far smaller than a light wave.
- **Visual:** A field of small charcoal paper dots labelled N₂ and O₂. A magnifier circle held by Pip enlarges one molecule next to a teal wave to compare size. Label: "molecule ≪ wave".
- **Motion:** Entrance: the dots pop in with a stagger. Primary action: the beam threads through the dots. Secondary reaction: Pip steps in with the magnifier. Exit: the camera dives into the magnifier.
- **Voiceover:** "To reach your eyes, it has to cross the air: trillions of nitrogen and oxygen molecules, far smaller than any wave."
- **Sound:** Paper-dot pops tuned to the scale, and a lens "thwip" when the magnifier arrives.
- **Transition:** The magnifier lens grows to fill the frame. Its molecule becomes the centre of the next diagram.

### SCENE 4 — 0:31–0:47 · Mechanism
- **Learning purpose:** A molecule scatters light in new directions, and shorter waves scatter much more (about 5× for blue compared with red).
- **Visual:** One large molecule in the centre. A red wave passes almost straight through with only faint side-rays. A blue wave arrives and throws out strong teal rays in every direction. On the right, two torn-paper bars rise: red at 1×, blue at about 5×. Label: "scattering".
- **Motion:** Entrance: the red wave enters from the left. Primary action: the blue wave hits and the rays burst out. Secondary reaction: the bars grow and Pip hops at the tall blue bar. Exit: the teal rays stretch outward.
- **Voiceover:** "When a wave meets a molecule, it gets bounced off in a new direction. That's scattering. And short waves scatter much more than long ones. Blue scatters about five times more than red."
- **Sound:** A soft bounce "tok" when the red wave touches, a bright spray of pings for the blue burst, and a rising two-note tick as the bars grow.
- **Transition:** The scattered teal rays grow long and become the light paths across a whole sky.

### SCENE 5 — 0:47–1:03 · Discovery
- **Learning purpose:** Scattered blue arrives from every direction, so the whole sky looks blue. A short note explains why the sky isn't violet.
- **Visual:** The landscape again. A beam passes overhead. Dozens of molecule dots each send teal paths down toward Pip's eyes from all angles. Teal gouache floods the sky card. A small violet strip appears with an eye icon and the label "violet: less of it, eyes less keen".
- **Motion:** Entrance: the camera pulls back from the rays. Primary action: paths arrive at Pip from all angles and the sky wash fills. Secondary reaction: Pip turns its eyes around the sky, then does a happy hop. Exit: the sun starts to sink.
- **Voiceover:** "So blue gets bounced all across the sky, and from every direction some of it heads to you. Violet scatters even more, but sunlight has less of it, and our eyes favour blue."
- **Sound:** The music opens up with a warm pad and adds a discovery chime. Faint pings play as the paths arrive.
- **Transition:** The mustard sun slides down toward the horizon, and the scene becomes the evening version of the same landscape.

### SCENE 6 — 1:03–1:15 · Consequence
- **Learning purpose:** At sunset, light crosses much more air, so most of the blue scatters away before it arrives.
- **Visual:** A curved Earth edge with a band of atmosphere. Two paths: a noon path (short, straight down) and a sunset path (long, grazing). Along the sunset path, teal ribbons peel off, and what reaches Pip is coral and mustard. The sky wash turns coral and mustard. Labels: "noon: short path" and "sunset: long path".
- **Motion:** Entrance: the Earth arc rises. Primary action: teal peels away along the long path. Secondary reaction: Pip's colour warms and Pip blinks. Exit: the diagram tidies into two panels.
- **Voiceover:** "At sunset, light skims through far more air. Most of the blue is scattered away before it arrives, leaving reds and oranges."
- **Sound:** A long filtered whoosh along the path, small paper-peel ticks, and the music drops into a warmer key.
- **Transition:** The two paths fold flat into the two recap panels.

### SCENE 7 — 1:15–1:26 · Recap
- **Learning purpose:** Fix the single rule in memory.
- **Visual:** Two panels side by side: "day" (short path, teal sky) and "sunset" (long path, coral sky). Across the top is a crayon banner: "short waves scatter most". Pip waves.
- **Motion:** Entrance: the panels settle. Primary action: the banner is written on stroke by stroke. Secondary reaction: Pip waves and blinks. Exit: the terminal shows `lesson complete ✓` and the window fades.
- **Voiceover:** "Short waves scatter most. That's why the sky is blue by day, and glows red at sunset."
- **Sound:** The full marimba motif resolves to the tonic, with a soft end chime.
- **Transition:** End card.

## 5. Final voiceover (≈170 words)

> Look up on a clear day. The sky is blue — but sunlight is white. So where does the blue come from?
> Sunlight is every colour travelling together. Each colour is a wave: red with long, lazy wiggles, blue with short, quick ones.
> To reach your eyes, it has to cross the air: trillions of nitrogen and oxygen molecules, far smaller than any wave.
> When a wave meets a molecule, it gets bounced off in a new direction. That's scattering. And short waves scatter much more than long ones. Blue scatters about five times more than red.
> So blue gets bounced all across the sky, and from every direction some of it heads to you. Violet scatters even more, but sunlight has less of it, and our eyes favour blue.
> At sunset, light skims through far more air. Most of the blue is scattered away before it arrives, leaving reds and oranges.
> Short waves scatter most. That's why the sky is blue by day, and glows red at sunset.

Each line is timed for 125–145 wpm within its scene, with space left for the key changes to land.

**Accuracy notes.** Rayleigh scattering intensity ∝ 1/λ⁴. For blue (~450 nm) compared with red (~680 nm), that gives (680/450)⁴ ≈ 5.2, so "about five times". N₂ and O₂ molecules are about 0.3 nm across, roughly a thousand times smaller than visible wavelengths (400–700 nm), which is what puts us in the Rayleigh regime. The sky is not violet for three reasons: the solar spectrum holds less violet, some violet is absorbed high in the atmosphere, and human cones respond weakly to violet. The script keeps the first and last of these.

## 6. Transition map

| From → To | Physical carrier |
|---|---|
| 1 → 2 | The sun's glow narrows into a white **beam** |
| 2 → 3 | The colour waves **recombine** into a beam that enters the dots |
| 3 → 4 | The **magnifier lens** grows to fill the frame and its molecule becomes the diagram's centre |
| 4 → 5 | The scattered **rays stretch** into paths across the sky |
| 5 → 6 | The **sun sinks** to the horizon and the same landscape turns to evening |
| 6 → 7 | The noon and sunset **paths fold** into the two recap panels |

## 7. Sound plan

- **Music:** A marimba and pluck arpeggio in C major pentatonic at 96 BPM. A pad joins at the Discovery scene. The piece moves to A minor pentatonic (warmer) at sunset and resolves to C at the recap. Level is −18 LUFS under voice.
- **Ambience:** A low-passed wind bed at −30 dB. It thins inside the molecule close-ups.
- **Tactile SFX, synced to motion:** paper slide (layer entrances), pop ("?", molecule dots), glass chime (prism), bounce tok/pings (scattering), rising ticks (bars), peel ticks (sunset), end chime.
- **Mix rule:** Nothing louder than the voice. SFX land on the frame where the motion's contact happens.

## 8. Technical implementation

- `index.html` is a self-contained Canvas 2D renderer. `renderFrame(t)` is a **pure function of time**, so the same `t` always gives the same frame, boil included. The boil uses a seeded hash of `(shapeId, floor(t·8))`.
- The player has play/pause, a scrubber, a captions toggle and an optional browser-voice narration (Web Speech API), and it scales to any viewport. Audio in the player is synthesised live with Web Audio from the same cue list as the video.
- `render/` holds the offline pipeline (`build.sh` runs all of it). Playwright drives headless Chromium and captures all 2,064 frames at 1920×1080. `audio.py` synthesises the music, ambience and SFX, plus a scratch voiceover (espeak-ng + MBROLA) that is placed phrase by phrase on each caption. `mux.sh` muxes H.264 video, AAC audio and a soft caption track into `out/sky-is-blue.mp4`. Captions are also burned into the terminal bar. It also writes a music-and-effects-only version, `sky-is-blue_music-fx.mp4`.
- The scratch VO is a robotic timing guide, not the final voice. To swap it for a real read, record the seven lines in §5 as `render/vo/line_1.wav` … `line_7.wav` and re-run `python3 audio.py && ./mux.sh`. Each line is fitted to its cue in `timeline.json`.
