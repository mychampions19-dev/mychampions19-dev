# Morning Routine Video: Production Pack

Full-screen 16:9 overlays at 1080p / 30fps, edited in CapCut. **Status: Section 1 test run.**

## Folder layout
```
morning-routine-video/
├── 01_script/            Script_v2_Corrected.md  (with change log)
├── 02_flow_prompts/      Google Flow prompts, one file per section
│   └── characters/       ← save your Flow character images here
├── 03_graphics/
│   └── S01_MetabolicSwitch/   ← every clip for Section 1 (mine + your Flow clips)
├── 04_audio/             Beth voice files, one per section
└── _build/               source code for the motion graphics (ignore)
```

---

## FILE NAMING: rename every file as soon as you download it

**Pattern:** `S{section}-B{beat}_{TYPE}_{ShortName}_v{version}.mp4`

| Part | Meaning | Example |
|---|---|---|
| `S01` | Section number, 2 digits | `S01` … `S09` |
| `B03` | Beat number within the section, in script order | `B01`, `B02` … |
| `TYPE` | `MG` = motion graphic (made by Claude) · `3D` = Google Flow video · `IMG` = Flow still image · `HOST` = host on camera · `VO` = voice-over | `3D` |
| `ShortName` | 1–3 words in CamelCase, **copied exactly from the prompt heading** | `VisceralFatHug` |
| `v1` | Version. Keep the best take as the highest number | `v1`, `v2` |

**Examples**
- `S01-B03_3D_VisceralFatHug_v1.mp4`: your first Flow take of beat 3
- `S01-B03_3D_VisceralFatHug_v2.mp4`: a re-roll you prefer
- `S01-B06_MG_BurnVsStore_v1.mp4`: my motion graphic
- `CHAR-01_Cortisol_v1.png`: character sheet images (in `02_flow_prompts/characters/`)
- `S01_VO_Beth_v1.mp3`: final voice for Section 1

**Rules**
1. No spaces. Use `_` between parts and `-` only between section and beat.
2. Because names start with section and beat, sorting a folder by name puts the clips **in timeline order**.
3. Takes you don't use go in a `_rejects` subfolder, never deleted, in case you change your mind.
4. Each section gets its own folder, named `S01_MetabolicSwitch`, `S02_Phone`, and so on.

---

## SECTION 1 TIMING SHEET

Timecodes match Beth's test read (`04_audio/S01_Beth_TestRead.mp3`, 59.8 s). If your final voice take is paced differently, slide each clip so its **sync point** lands on the listed word.

| Beat | Timeline in → out | Clip | Trim | Sync point (the word the key moment hits) |
|---|---|---|---|---|
| B01 | 00:00.0 → 00:07.6 | **HOST** | — | "Most people assume…" |
| B02 | 00:07.6 → 00:13.3 | `S01-B02_MG_9AMSwitch_v1` | use first 5.7 s | switch flips to STORE on **"switch"** (clip 3.9 s) |
| B03 | 00:13.3 → 00:18.7 | `S01-B03_3D_VisceralFatHug_v1` *(you, Flow)* | use first 5.4 s | fat hugs organs on **"vital organs"** |
| B04 | 00:18.7 → 00:25.4 | `S01-B04_MG_ZeroCalories_v1` | use first 6.7 s | "0" slams on **"single calorie"** (clip 2.85 s) |
| B05 | 00:25.4 → 00:33.3 | `S01-B05_3D_CortisolAlarm_v1` *(you, Flow)* | use 7.9 s | alarm slam on **"stress hormones"** |
| B06 | 00:33.3 → 00:43.6 | `S01-B06_MG_BurnVsStore_v1` | use first 10.3 s | lever → BURN on **"burn"** (6.55 s); lever → STORE on **"lock"** (8.35 s) |
| B07 | 00:43.6 → 00:48.8 | `S01-B07_MG_7MistakesPreview_v1` | use first 5.2 s | "7" slams on **"seven"** (clip 1.3 s) |
| B08 | 00:48.8 → 00:59.8 | **HOST** | — | "We'll look at the actual science…" |

**Host on screen in Section 1: 18.6 s of 59.8 s (31%). Graphics: 69%.**

`S01_PREVIEW_Animatic_WithVoice.mp4` is the whole section cut together with Beth's voice, with placeholders where the host and the Flow shots go. Watch that first.

---

## CAPCUT SETUP
1. **Main track:** host footage. **Audio track 1:** Beth's voice.
2. **Overlay track, above the host:** drop each MG/3D clip at its timeline point. Right-click → *Fit to canvas*. They are already 1920×1080, so they cover the host completely.
3. **Sound effects** are baked into each MG clip. Leave them as they are (mixed to sit under the voice), or select the clip → Audio → Volume to taste.
4. **Flow clips:** select → Audio → Volume 0 (mute Veo's generated sound).
5. **Cuts:** straight cuts are fine because every MG clip opens with its own zoom-punch. For extra polish, use CapCut's "Zoom in" or "Pull in" transition on host → graphic cuts only.
