# Morning Routine Video: Production Pack

Full-screen 16:9 overlays at 1080p / 30fps, edited in CapCut. **Status: all graphics and all Flow shots done. Only host footage + final voice remain.**

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
- `S01-B06_MG_BurnVsStore_v2.mp4`: my motion graphic
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
| B03 | 00:13.3 → 00:18.7 | `S01-B03_3D_VisceralFatHug_v1` ✅ | **use 2.4 s → 7.8 s** of the Flow clip (skip the slow start) | fat hugs organs on **"vital organs"** |
| B04 | 00:18.7 → 00:25.4 | `S01-B04_MG_ZeroCalories_v2` (green counter) | use first 6.7 s | "0" slams on **"single calorie"** (clip 2.85 s) |
| B05 | 00:25.4 → 00:33.3 | `S01-B05_3D_CortisolAlarm_v1` ✅ | use 0 → 7.9 s | alarm slam on **"stress hormones"** |
| B06 | 00:33.3 → 00:43.6 | `S01-B06_MG_BurnVsStore_v2` | use first 10.3 s | lever → BURN on **"burn"** (6.55 s); lever → STORE on **"lock"** (8.35 s) |
| B07 | 00:43.6 → 00:48.8 | `S01-B07_MG_7MistakesPreview_v1` | use first 5.2 s | "7" slams on **"seven"** (clip 1.3 s) |
| B08 | 00:48.8 → 00:59.8 | **HOST** | — | "We'll look at the actual science…" |

**Host on screen in Section 1: 18.6 s of 59.8 s (31%). Graphics: 69%.**

`S01_PREVIEW_Animatic_WithVoice_LATEST.mp4` is the whole section cut together with Beth's voice and your Flow shots. Only the host segments are still placeholders. Older versions are in `_rejects/`. Each section folder has one `_LATEST` animatic.

Flow clips are 24 fps and my graphics are 30 fps. CapCut mixes them without any problem.

---

## SECTION 2 TIMING SHEET: Mistake #1, Phone (`03_graphics/S02_Phone/`)

Timecodes match `04_audio/S02_Beth_TestRead.mp3` (78.0 s). Word timings are in `04_audio/S02_word_timings.tsv`.

| Beat | Timeline in → out | Clip | Trim | Sync point |
|---|---|---|---|---|
| B01 | 00:00.0 → 00:04.9 | `S02-B01_MG_Mistake1Title_v1` | first 4.9 s | "#1" slams on **"one"** (1.0 s) |
| B02 | 00:04.9 → 00:09.7 | `S02-B02_3D_PhoneAlarmWake_v1` ✅ | **use 3.2 s → 8.0 s** | phone grabbed on **"grabbing that screen"** |
| B03 | 00:09.7 → 00:15.7 | `S02-B03_MG_NotificationStorm_v1` | first 6.0 s | cards on **"emails"** / **"news"** / **"social"** |
| B04 | 00:15.7 → 00:17.6 | **HOST** | — | "Here's why that's a biological problem." |
| B05 | 00:17.6 → 00:25.7 | `S02-B05_MG_CortisolCurve_v1` | first 8.1 s | band on **"30 to 45"**; title on **"Cortisol Awakening Response"** |
| B06 | 00:25.7 → 00:27.7 | `S02-B06_3D_BrainEngineStart_v1` ✅ | **use 3.4 s → 5.4 s** (720p file, CapCut scales it) | **"engine start"** |
| B07 | 00:27.7 → 00:36.3 | `S02-B07_MG_StressSurge_v1` | first 8.6 s | spikes on **"emails"** / **"news"**; flood on **"flood"** |
| B08 | 00:36.3 → 00:46.8 | `S02-B08_MG_StudyPNASNexus_v1` | first 10.5 s | journal on **"PNAS Nexus"**; 🚫 on **"block"**; 2 WEEKS on **"two weeks"** |
| B09 | 00:46.8 → 00:53.0 | **HOST** | — | "In just 14 days…" |
| B10 | 00:53.0 → 00:58.2 | `S02-B10_MG_TenYearsYounger_v1` | first 5.2 s | −10 YEARS on **"ten years"** |
| B11 | 00:58.2 → 01:04.4 | **HOST** | — | "When you flood your system…" |
| B12 | 01:04.4 → 01:07.1 | `S02-B12_MG_SurvivalVsFatBurn_v1` | first 2.7 s | ❌ on **"cannot operate"** |
| B13 | 01:07.1 → 01:10.5 | `S01-B03_3D_VisceralFatHug_v1` *(reused)* | **4.6 s → 7.9 s** | "wrapped around your internal organs" |
| B14 | 01:10.5 → 01:14.2 | `S02-B14_MG_3xReceptors_v1` | first 3.7 s | 3× on **"three times"** |
| B15 | 01:14.2 → 01:18.0 | `S02-B15_3D_CortisolDirectsFat_v1` ✅ | **use 4.0 s → 7.9 s** | "store fat right in your midsection" |

**Host on screen in Section 2: 14.3 s of 78 s (18%).**

## SECTION 3 TIMING SHEET: Mistake #2, Caffeine Before Hydration (`03_graphics/S03_Caffeine/`)

Timecodes match `04_audio/S03_Beth_TestRead.mp3` (45.7 s). Word timings are in `04_audio/S03_word_timings.tsv`.

| Beat | Timeline in → out | Clip | Trim | Sync point |
|---|---|---|---|---|
| B01 | 00:00.0 → 00:03.0 | `S03-B01_MG_Mistake2Title_v1` | first 3.0 s | "#2" on **"two"** |
| B02 | 00:03.0 → 00:10.0 | `S03-B02_MG_OvernightDehydration_v1` | first 7.0 s | 7 · 8 · 9 on **"seven, eight, or nine"** |
| B03 | 00:10.0 → 00:15.4 | `S03-B03_3D_DehydratedBlood_v1` ✅ | **use 2.0 s → 7.4 s** | "more concentrated" |
| B04 | 00:15.4 → 00:17.4 | **HOST** | — | "So what do most people reach for first?" |
| B05 | 00:17.4 → 00:23.1 | `S03-B05_MG_CaffeineStressedSystem_v1` | first 5.7 s | CAFFEINE! on **"Caffeine"**; badges on **"dehydrated"** / **"cortisol-elevated"** |
| B06 | 00:23.1 → 00:27.3 | `S03-B06_3D_GasolineOnFire_v1` ✅ | **use 3.6 s → 7.8 s** (pour → fireball → frazzled gremlin) | **"gasoline onto a flickering fire"** |
| B07 | 00:27.3 → 00:30.6 | `S03-B07_MG_JitteryCrash_v1` | first 3.3 s | JITTERY on **"9:30 AM"**; CRASH on **"crashing"** |
| B08 | 00:30.6 → 00:32.4 | **HOST** | — | "Here's a key metabolic insight:" |
| B09 | 00:32.4 → 00:39.7 | `S03-B09_MG_HungerMask_v1` | first 7.3 s | mask flies off on **"wearing a mask"** |
| B10 | 00:39.7 → 00:45.7 | `S03-B10_MG_HydrateFirst_v1` | first 6.0 s | ✅ on **"energy"** / **"appetite"** |

**Host on screen in Section 3: 3.8 s of 45.7 s (8%).**

## SECTION 4 TIMING SHEET: Mistake #3, Skipping Morning Light (`03_graphics/S04_MorningLight/`)

Timecodes match `04_audio/S04_Beth_TestRead.mp3` (43.3 s). Word timings are in `04_audio/S04_word_timings.tsv`.

| Beat | Timeline in → out | Clip | Trim | Sync point |
|---|---|---|---|---|
| B01 | 00:00.0 → 00:05.3 | `S04-B01_MG_Mistake3Title_v1` | first 5.3 s | "#3" on **"three"** |
| B02 | 00:05.3 → 00:08.9 | `S04-B02_3D_BrainMasterClock_v1` ✅ | **use 1.8 s → 5.4 s** (key turn → gears → pull-back) | "master clock… circadian rhythm" |
| B03 | 00:08.9 → 00:19.0 | `S04-B03_MG_CircadianClock_v1` | first 10.1 s | ☀️ on **"cortisol"**; 🌙 on **"melatonin"**; arc on **"insulin"**; INSULIN card on **"Insulin is…"** |
| B04 | 00:19.0 → 00:23.8 | `S04-B04_MG_OutOfSync_v1` | first 4.8 s | gears jam on **"out of alignment"**; gauge drops on **"drops significantly"** |
| B05 | 00:23.8 → 00:28.4 | **HOST** | — | "Studies link bright light early in the day…" |
| B06 | 00:28.4 → 00:31.9 | `S04-B06_3D_FluorescentGloom_v1` ✅ | **use 0.3 s → 3.8 s** (4 s clip) | "dim artificial lighting or fluorescent bulbs" |
| B07 | 00:31.9 → 00:35.5 | `S04-B07_MG_NoSignal_v1` | first 3.6 s | NO SIGNAL on **"never receives"** |
| B08 | 00:35.5 → 00:43.3 | `S04-B08_MG_LightReset_v1` | first 7.8 s | reset on **"master reset"**; ✅ on **"blood sugar"** / **"metabolism"** |

**Host on screen in Section 4: 4.6 s of 43.3 s (10%).**

## SECTION 5 TIMING SHEET: Mistake #4, High-Carb Breakfast (`03_graphics/S05_HighCarbBreakfast/`)

Timecodes match `04_audio/S05_Beth_TestRead.mp3` (70.7 s). Word timings are in `04_audio/S05_word_timings.tsv`.

| Beat | Timeline in → out | Clip | Trim | Sync point |
|---|---|---|---|---|
| B01 | 00:00.0 → 00:06.4 | `S05-B01_MG_Mistake4Title_v1` | first 6.4 s | "#4" on **"four"** |
| B02 | 00:06.4 → 00:10.7 | `S05-B02_MG_HealthyBreakfastLineup_v1` | first 4.3 s | each food pops on its word |
| B03 | 00:10.7 → 00:17.1 | `S05-B03_3D_DessertInDisguise_v1` ✅ | **use 1.2 s → 7.5 s** (reveal lands ~3.3 s in) | unmasking on **"dessert in disguise"** |
| B04 | 00:17.1 → 00:28.5 | `S05-B04_MG_GlucoseSurge_v1` | first 11.4 s | STABLE on **"baseline stable"**; SURGE on **"surge"**; insulin on **"pancreas"** |
| B05 | 00:28.5 → 00:32.1 | `S05-B05_MG_FatBurnSuppressed_v1` | first 3.6 s | lock on **"fat burning"**; stamp on **"suppressed"** |
| B06 | 00:32.1 → 00:36.5 | `S05-B06_MG_SugarCrash_v1` | first 4.4 s | CRASH on **"crash below baseline"** |
| B07 | 00:36.5 → 00:42.4 | `S05-B07_MG_CrashSymptoms_v1` | first 5.9 s | cards on **"shakiness"** / **"brain fog"** / **"signal"** |
| B08 | 00:42.4 → 00:45.2 | `S05-B08_3D_SugarRollercoaster_v1` ✅ | **use 1.0 s → 3.8 s** (4 s clip) | "blood sugar rollercoaster" |
| B09 | 00:45.2 → 00:48.0 | **HOST** | — | "Contrast that with research from the University of Missouri." |
| B10 | 00:48.0 → 01:01.4 | `S05-B10_MG_fMRICravingsStudy_v1` | first 13.4 s | scans on **"high-protein"** / **"high-carb"**; CRAVINGS on **"food cravings"** |
| B11 | 01:01.4 → 01:10.7 | `S05-B11_MG_EggsVsBagel_v1` | first 9.3 s | EGGS on **"egg-based"**; BAGEL on **"bagel"** |

**Host on screen in Section 5: 2.8 s of 70.7 s (4%).**

## SECTION 6 TIMING SHEET: Mistakes #5 & #6, Eating Too Soon & Sitting After (`03_graphics/S06_EatingAndSitting/`)

Timecodes match `04_audio/S06_Beth_TestRead.mp3` (55.1 s). Word timings are in `04_audio/S06_word_timings.tsv`. They are hand-checked after 28 s, where the automatic timings drifted.

| Beat | Timeline in → out | Clip | Trim | Sync point |
|---|---|---|---|---|
| B01 | 00:00.0 → 00:04.9 | `S06-B01_MG_Mistakes5and6_v1` | first 4.9 s | tiles on **"five and six"**; gauge cracks on **"sabotage"** |
| B02 | 00:04.9 → 00:08.4 | `S06-B02_MG_Mistake5Title_v1` | first 3.5 s | "#5" on **"five"** |
| B03 | 00:08.4 → 00:14.1 | `S06-B03_MG_OvernightFatBurning_v1` | first 5.7 s | gauge drops on **"drops to baseline"**; ⚡ on **"energy"** |
| B04 | 00:14.1 → 00:19.8 | `S06-B04_3D_WindowSlam_v6` ✅ | **use 0.3 s → 6.0 s** (6 s clip) | slam on **"slam that fat-burning window shut"** |
| B05 | 00:19.8 → 00:25.9 | `S06-B05_MG_PushMealBack_v1` | first 6.1 s | 💧 on **"hydrate"**; 🚶 on **"move"** |
| B06 | 00:25.9 → 00:28.8 | `S06-B06_MG_Mistake6Title_v1` | first 2.9 s | "#6" on **"six"** |
| B07 | 00:28.8 → 00:33.4 | **HOST** | — | "When you finish a meal and sit directly at a desk…" |
| B08 | 00:33.4 → 00:36.4 | `S06-B08_MG_InsulinForcesStorage_v1` | first 3.0 s | cubes into 📦 on **"storage"** |
| B09 | 00:36.4 → 00:46.2 | `S06-B09_MG_WalkingStudy_v1` | first 9.8 s | journal on **"Diabetes Care"**; ✅ on **"as effectively"** |
| B10 | 00:46.2 → 00:52.5 | `S06-B10_3D_MuscleSideDoor_v6` ✅ | **use 1.6 s → 8.0 s** | "Why? Because when your leg muscles contract…" |
| B11 | 00:52.5 → 00:55.1 | `S06-B11_MG_InsulinFreeSideDoor_v1` | first 2.5 s | **"insulin-free side door"** |

**Host on screen in Section 6: 4.7 s of 55.1 s (8%).**

## SECTION 7 TIMING SHEET: Mistake #7, Survival Mode (`03_graphics/S07_SurvivalMode/`)

Timecodes match `04_audio/S07_Beth_TestRead.mp3` (37.2 s). Word timings are in `04_audio/S07_word_timings.tsv`.

| Beat | Timeline in → out | Clip | Trim | Sync point |
|---|---|---|---|---|
| B01 | 00:00.0 → 00:04.9 | `S07-B01_MG_Mistake7Title_v1` | first 4.9 s | "#7" on **"seventh"** |
| B02 | 00:04.9 → 00:11.4 | `S07-B02_MG_StressStack_v1` | first 6.5 s | blocks land on **"phone"** / **"caffeine"** / **"dark"** / **"stress before 8 AM"** |
| B03 | 00:11.4 → 00:14.3 | `S07-B03_3D_BrainDanger_v7` ✅ | **use 0.6 s → 3.5 s** (alarms go red → panic) | **"danger"** |
| B04 | 00:14.3 → 00:17.2 | `S07-B04_MG_AdrenalFlood_v1` | first 2.9 s | flood on **"flood your system"** |
| B05 | 00:17.2 → 00:20.6 | `S07-B05_3D_CavemanThreat_v7` ✅ | **use 0.6 s → 4.0 s** (tiger leaps → brain freezes) | "evolutionary… under threat" |
| B06 | 00:20.6 → 00:23.1 | `S07-B06_MG_SurvivalPriority_v1` | first 2.5 s | ✅ on **"survival"**; ❌ on **"not fat loss"** |
| B07 | 00:23.1 → 00:28.5 | `S07-B07_MG_ProtectiveFatRisks_v1` | first 5.5 s | fat wraps on **"heart, liver, kidneys"** |
| B08 | 00:28.5 → 00:32.6 | **HOST** | — | "…it's rarely a lack of willpower." |
| B09 | 00:32.6 → 00:37.2 | `S07-B09_MG_RoutineSignalsSurvival_v1` | first 4.6 s | needle to STORE on **"survival stress"** |

**Host on screen in Section 7: 4.1 s of 37.2 s (11%).**

## SECTION 8 TIMING SHEET: The 7-Step Blueprint (`03_graphics/S08_Blueprint/`)

Timecodes match `04_audio/S08_Beth_TestRead.mp3` (102.7 s). Word timings are in `04_audio/S08_word_timings.tsv`.

| Beat | Timeline in → out | Clip | Trim | Sync point |
|---|---|---|---|---|
| B01 | 00:00.0 → 00:04.4 | `S08-B01_MG_FlipTheScript_v1` | first 4.4 s | switch flips to BURN on **"flip the script"** |
| B02 | 00:04.4 → 00:13.6 | `S08-B02_MG_BlueprintOverview_v1` | first 9.2 s | title on **"7-Step"**; pills on **"metabolism"** / **"hormones"** / **"fat-burning machine"** |
| B03 | 00:13.6 → 00:23.8 | `S08-B03_MG_Step1PhoneOff_v1` | first 10.2 s | "1" on **"Step 1"** |
| B04 | 00:23.8 → 00:33.4 | `S08-B04_MG_Step2Hydrate_v1` | first 9.6 s | "2" on **"Step 2"** |
| B05 | 00:33.4 → 00:38.3 | `S08-B05_3D_HydratedBlood_v1` ✅ | **use 1.6 s → 6.4 s** (water wave → cells plump up) | "Rehydrating blood volume…" |
| B06 | 00:38.3 → 00:45.6 | `S08-B06_MG_Step3Sunlight_v1` | first 7.3 s | "3" on **"Step 3"** |
| B07 | 00:45.6 → 00:52.6 | **HOST** | — | "This sets your master circadian clock…" |
| B08 | 00:52.6 → 00:57.4 | `S08-B08_MG_Step4Walk_v1` | first 4.7 s | "4" on **"Step 4"** |
| B09 | 00:57.4 → 01:01.9 | `S08-B09_3D_SunriseWalk_v8` ✅ | **use 0.8 s → 5.3 s** | "Walking clears morning blood sugar…" |
| B10 | 01:01.9 → 01:09.8 | `S08-B10_MG_Step5CoffeeLater_v1` | first 7.9 s | "5" on **"Step 5"** |
| B11 | 01:09.8 → 01:16.9 | `S08-B11_MG_SmoothEnergy_v1` | first 7.1 s | ✨ on **"smoother, cleaner energy"** |
| B12 | 01:16.9 → 01:26.7 | `S08-B12_MG_Step6ProteinFirst_v1` | first 9.8 s | "6" on **"Step 6"**; foods on their words |
| B13 | 01:26.7 → 01:29.6 | **HOST** | — | "This stabilizes blood sugar…" |
| B14 | 01:29.6 → 01:33.7 | `S08-B14_MG_Step7Calm_v1` | first 4.1 s | "7" on **"Step 7"** |
| B15 | 01:33.7 → 01:38.2 | `S08-B15_MG_Breathing_v1` | first 4.5 s | "deep nasal breathing" |
| B16 | 01:38.2 → 01:42.7 | `S08-B16_3D_BrainCalm_v8` ✅ | **use 1.2 s → 5.7 s** (fireplace lights → fat melts to sparkles) | "Shift your nervous system…" |

**Host on screen in Section 8: 10.0 s of 102.7 s (10%).**

## SECTION 9 TIMING SHEET: Outro (`03_graphics/S09_Outro/`)

Timecodes match `04_audio/S09_Beth_TestRead.mp3` (21.8 s).

| Beat | Timeline in → out | Clip | Trim | Sync point |
|---|---|---|---|---|
| B01 | 00:00.0 → 00:03.7 | **HOST** | — | "Your metabolism isn't broken…" |
| B02 | 00:03.7 → 00:12.4 | `S09-B02_MG_ChangeTheSignals_v1` | first 8.7 s | ❌ on **"stress and sugar"**; tiles on **"hydration, light, movement, protein"** |
| B03 | 00:12.4 → 00:15.4 | `S09-B03_MG_FatBurningOn_v1` | first 3.0 s | switch on **"turning on fat burning"** |
| B04 | 00:15.4 → 00:21.8 | **HOST** | — | "Pick just two or three of these steps…" (ends on the host) |

**Host on screen in Section 9: 10.1 s of 21.8 s (46%). The ending belongs to her.**

---

## WHOLE VIDEO AT A GLANCE

| Section | Length | Host on screen | Code graphics (done) | Flow shots (you) |
|---|---|---|---|---|
| S01 Metabolic Switch | 0:60 | 31% | 4 | 2 ✅ |
| S02 Phone | 1:18 | 18% | 8 | 3 (+1 reused) |
| S03 Caffeine | 0:46 | 8% | 6 | 2 |
| S04 Morning Light | 0:43 | 10% | 5 | 2 |
| S05 High-Carb Breakfast | 1:11 | 4% | 8 | 2 |
| S06 Eating & Sitting | 0:55 | 8% | 8 | 2 |
| S07 Survival Mode | 0:37 | 11% | 6 | 2 |
| S08 Blueprint | 1:43 | 10% | 11 | 3 |
| S09 Outro | 0:22 | 46% | 2 | 0 |
| **Total** | **≈ 8:35** | **≈ 14%** | **58** | **16 new** |

### FLOW CHECKLIST: every shot still to generate
**New characters first (save to Ingredients):** CHAR-05_Brain ✅ · CHAR-06_Coffee ✅ · CHAR-07_Muscle ✅ · CHAR-08_Glucose ✅

- [x] S02-B02_3D_PhoneAlarmWake · [x] S02-B06_3D_BrainEngineStart · [x] S02-B15_3D_CortisolDirectsFat
- [x] S03-B03_3D_DehydratedBlood · [x] S03-B06_3D_GasolineOnFire
- [x] S04-B02_3D_BrainMasterClock · [x] S04-B06_3D_FluorescentGloom
- [x] S05-B03_3D_DessertInDisguise · [x] S05-B08_3D_SugarRollercoaster
- [x] S06-B04_3D_WindowSlam · [x] S06-B10_3D_MuscleSideDoor
- [x] S07-B03_3D_BrainDanger · [x] S07-B05_3D_CavemanThreat
- [x] S08-B05_3D_HydratedBlood · [x] S08-B09_3D_SunriseWalk · [x] S08-B16_3D_BrainCalm

Prompts are in `02_flow_prompts/` (one file per section). Send the clips back and I'll cut them into the animatics.

**Note on length:** Beth reads quickly, so the full script comes to about 8½ minutes, under your 10–12 minute target. Options: slow Beth down slightly in ElevenLabs (Speed around 0.9 adds roughly a minute), let the host ad-lib between sections, or add a short new section. Say which you prefer and I'll re-time everything.

## CAPCUT SETUP
1. **Main track:** host footage. **Audio track 1:** Beth's voice.
2. **Overlay track, above the host:** drop each MG/3D clip at its timeline point. Right-click → *Fit to canvas*. They are already 1920×1080, so they cover the host completely.
3. **Sound effects** are baked into each MG clip. Leave them as they are (mixed to sit under the voice), or select the clip → Audio → Volume to taste.
4. **Flow clips:** select → Audio → Volume 0 (mute Veo's generated sound).
5. **Cuts:** straight cuts are fine because every MG clip opens with its own zoom-punch. For extra polish, use CapCut's "Zoom in" or "Pull in" transition on host → graphic cuts only.
