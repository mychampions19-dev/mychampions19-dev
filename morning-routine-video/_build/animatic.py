"""Assemble a section animatic: voice + MG clips (with their SFX) + Flow clips (muted) + placeholders.
Usage: python3 animatic.py S02
Segments: (kind, source, clip_in, duration)
  kind 'mg'  → our motion graphic (keeps its SFX)
  kind '3d'  → Flow clip (muted); if file missing, a placeholder card is used
  kind 'host'→ host placeholder card"""
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJ = ROOT.parent
G = PROJ / "03_graphics"
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"

SECTIONS = {
    "S01": dict(folder="S01_MetabolicSwitch", voice="04_audio/S01_Beth_TestRead.mp3", segs=[
        ("host", None, 0, 7.6, "S01-B01 · \"Most people assume…\""),
        ("mg", "S01_MetabolicSwitch/S01-B02_MG_9AMSwitch_v1.mp4", 0, 5.7),
        ("3d", "S01_MetabolicSwitch/S01-B03_3D_VisceralFatHug_v1.mp4", 2.4, 5.4),
        ("mg", "S01_MetabolicSwitch/S01-B04_MG_ZeroCalories_v2.mp4", 0, 6.7),
        ("3d", "S01_MetabolicSwitch/S01-B05_3D_CortisolAlarm_v1.mp4", 0, 7.9),
        ("mg", "S01_MetabolicSwitch/S01-B06_MG_BurnVsStore_v2.mp4", 0, 10.3),
        ("mg", "S01_MetabolicSwitch/S01-B07_MG_7MistakesPreview_v1.mp4", 0, 5.2),
        ("host", None, 0, 11.0, "S01-B08 · \"We'll look at the actual science…\""),
    ]),
    "S02": dict(folder="S02_Phone", voice="04_audio/S02_Beth_TestRead.mp3", segs=[
        ("mg", "S02_Phone/S02-B01_MG_Mistake1Title_v1.mp4", 0, 4.93),
        ("3d", "S02_Phone/S02-B02_3D_PhoneAlarmWake_v1.mp4", 3.2, 4.81, "S02-B02_3D_PhoneAlarmWake — brain grabs the buzzing phone"),
        ("mg", "S02_Phone/S02-B03_MG_NotificationStorm_v1.mp4", 0, 5.97),
        ("host", None, 0, 1.91, "S02-B04 · \"Here's why that's a biological problem.\""),
        ("mg", "S02_Phone/S02-B05_MG_CortisolCurve_v1.mp4", 0, 8.07),
        ("3d", "S02_Phone/S02-B06_3D_BrainEngineStart_v1.mp4", 3.4, 2.03, "S02-B06_3D_BrainEngineStart — brain turns the ignition key"),
        ("mg", "S02_Phone/S02-B07_MG_StressSurge_v1.mp4", 0, 8.61),
        ("mg", "S02_Phone/S02-B08_MG_StudyPNASNexus_v1.mp4", 0, 10.47),
        ("host", None, 0, 6.19, "S02-B09 · \"In just 14 days…\""),
        ("mg", "S02_Phone/S02-B10_MG_TenYearsYounger_v1.mp4", 0, 5.24),
        ("host", None, 0, 6.17, "S02-B11 · \"When you flood your system…\""),
        ("mg", "S02_Phone/S02-B12_MG_SurvivalVsFatBurn_v1.mp4", 0, 2.74),
        ("3d", "S01_MetabolicSwitch/S01-B03_3D_VisceralFatHug_v1.mp4", 4.6, 3.34, "reused S01-B03"),
        ("mg", "S02_Phone/S02-B14_MG_3xReceptors_v1.mp4", 0, 3.73),
        ("3d", "S02_Phone/S02-B15_3D_CortisolDirectsFat_v1.mp4", 4.0, 3.9, "S02-B15_3D_CortisolDirectsFat — gremlin marshals direct fat to the belly"),
    ]),
    "S03": dict(folder="S03_Caffeine", voice="04_audio/S03_Beth_TestRead.mp3", segs=[
        ("mg", "S03_Caffeine/S03-B01_MG_Mistake2Title_v1.mp4", 0, 3.01),
        ("mg", "S03_Caffeine/S03-B02_MG_OvernightDehydration_v1.mp4", 0, 7.00),
        ("3d", "S03_Caffeine/S03-B03_3D_DehydratedBlood_v1.mp4", 2.0, 5.39, "S03-B03_3D_DehydratedBlood — crowded, sluggish blood cells"),
        ("host", None, 0, 1.97, "S03-B04 · \"So what do most people reach for first?\""),
        ("mg", "S03_Caffeine/S03-B05_MG_CaffeineStressedSystem_v1.mp4", 0, 5.68),
        ("3d", "S03_Caffeine/S03-B06_3D_GasolineOnFire_v1.mp4", 3.6, 4.20, "S03-B06_3D_GasolineOnFire — coffee cup pours onto the gremlin's fire"),
        ("mg", "S03_Caffeine/S03-B07_MG_JitteryCrash_v1.mp4", 0, 3.30),
        ("host", None, 0, 1.85, "S03-B08 · \"Here's a key metabolic insight:\""),
        ("mg", "S03_Caffeine/S03-B09_MG_HungerMask_v1.mp4", 0, 7.29),
        ("mg", "S03_Caffeine/S03-B10_MG_HydrateFirst_v1.mp4", 0, 6.01),
    ]),
    "S04": dict(folder="S04_MorningLight", voice="04_audio/S04_Beth_TestRead.mp3", segs=[
        ("mg", "S04_MorningLight/S04-B01_MG_Mistake3Title_v1.mp4", 0, 5.32),
        ("3d", "S04_MorningLight/S04-B02_3D_BrainMasterClock_v1.mp4", 1.8, 3.62, "S04-B02_3D_BrainMasterClock — brain winds the giant sun & moon clock"),
        ("mg", "S04_MorningLight/S04-B03_MG_CircadianClock_v1.mp4", 0, 10.07),
        ("mg", "S04_MorningLight/S04-B04_MG_OutOfSync_v1.mp4", 0, 4.83),
        ("host", None, 0, 4.56, "S04-B05 · \"Studies link bright light early in the day…\""),
        ("3d", "S04_MorningLight/S04-B06_3D_FluorescentGloom_v1.mp4", 0.3, 3.49, "S04-B06_3D_FluorescentGloom — brain stuck under a flickering office light"),
        ("mg", "S04_MorningLight/S04-B07_MG_NoSignal_v1.mp4", 0, 3.63),
        ("mg", "S04_MorningLight/S04-B08_MG_LightReset_v1.mp4", 0, 7.81),
    ]),
    "S05": dict(folder="S05_HighCarbBreakfast", voice="04_audio/S05_Beth_TestRead.mp3", segs=[
        ("mg", "S05_HighCarbBreakfast/S05-B01_MG_Mistake4Title_v1.mp4", 0, 6.41),
        ("mg", "S05_HighCarbBreakfast/S05-B02_MG_HealthyBreakfastLineup_v1.mp4", 0, 4.33),
        ("3d", "S05_HighCarbBreakfast/S05-B03_3D_DessertInDisguise_v1.mp4", 1.2, 6.32, "S05-B03_3D_DessertInDisguise — oatmeal bowl unmasks as a cake"),
        ("mg", "S05_HighCarbBreakfast/S05-B04_MG_GlucoseSurge_v1.mp4", 0, 11.39),
        ("mg", "S05_HighCarbBreakfast/S05-B05_MG_FatBurnSuppressed_v1.mp4", 0, 3.62),
        ("mg", "S05_HighCarbBreakfast/S05-B06_MG_SugarCrash_v1.mp4", 0, 4.41),
        ("mg", "S05_HighCarbBreakfast/S05-B07_MG_CrashSymptoms_v1.mp4", 0, 5.92),
        ("3d", "S05_HighCarbBreakfast/S05-B08_3D_SugarRollercoaster_v1.mp4", 1.0, 2.79, "S05-B08_3D_SugarRollercoaster — brain on a blood sugar rollercoaster"),
        ("host", None, 0, 2.77, "S05-B09 · \"Contrast that with research from the University of Missouri.\""),
        ("mg", "S05_HighCarbBreakfast/S05-B10_MG_fMRICravingsStudy_v1.mp4", 0, 13.41),
        ("mg", "S05_HighCarbBreakfast/S05-B11_MG_EggsVsBagel_v1.mp4", 0, 9.31),
    ]),
    "S06": dict(folder="S06_EatingAndSitting", voice="04_audio/S06_Beth_TestRead.mp3", segs=[
        ("mg", "S06_EatingAndSitting/S06-B01_MG_Mistakes5and6_v1.mp4", 0, 4.87),
        ("mg", "S06_EatingAndSitting/S06-B02_MG_Mistake5Title_v1.mp4", 0, 3.51),
        ("mg", "S06_EatingAndSitting/S06-B03_MG_OvernightFatBurning_v1.mp4", 0, 5.71),
        ("3d", "S06_EatingAndSitting/S06-B04_3D_WindowSlam_v1.mp4", 1.0, 5.67, "S06-B04_3D_WindowSlam — breakfast slams the fat-burning window shut"),
        ("mg", "S06_EatingAndSitting/S06-B05_MG_PushMealBack_v1.mp4", 0, 6.12),
        ("mg", "S06_EatingAndSitting/S06-B06_MG_Mistake6Title_v1.mp4", 0, 2.89),
        ("host", None, 0, 4.65, "S06-B07 · \"When you finish a meal and sit…\""),
        ("mg", "S06_EatingAndSitting/S06-B08_MG_InsulinForcesStorage_v1.mp4", 0, 2.97),
        ("mg", "S06_EatingAndSitting/S06-B09_MG_WalkingStudy_v1.mp4", 0, 9.78),
        ("3d", "S06_EatingAndSitting/S06-B10_3D_MuscleSideDoor_v1.mp4", 1.0, 6.37, "S06-B10_3D_MuscleSideDoor — muscle opens a side door for glucose"),
        ("mg", "S06_EatingAndSitting/S06-B11_MG_InsulinFreeSideDoor_v1.mp4", 0, 2.54),
    ]),
    "S07": dict(folder="S07_SurvivalMode", voice="04_audio/S07_Beth_TestRead.mp3", segs=[
        ("mg", "S07_SurvivalMode/S07-B01_MG_Mistake7Title_v1.mp4", 0, 4.85),
        ("mg", "S07_SurvivalMode/S07-B02_MG_StressStack_v1.mp4", 0, 6.51),
        ("3d", "S07_SurvivalMode/S07-B03_3D_BrainDanger_v1.mp4", 1.0, 2.93, "S07-B03_3D_BrainDanger — alarm lights, brain panics"),
        ("mg", "S07_SurvivalMode/S07-B04_MG_AdrenalFlood_v1.mp4", 0, 2.90),
        ("3d", "S07_SurvivalMode/S07-B05_3D_CavemanThreat_v1.mp4", 1.0, 3.36, "S07-B05_3D_CavemanThreat — caveman brain faces a sabre-tooth tiger"),
        ("mg", "S07_SurvivalMode/S07-B06_MG_SurvivalPriority_v1.mp4", 0, 2.52),
        ("mg", "S07_SurvivalMode/S07-B07_MG_ProtectiveFatRisks_v1.mp4", 0, 5.46),
        ("host", None, 0, 4.10, "S07-B08 · \"…it's rarely a lack of willpower.\""),
        ("mg", "S07_SurvivalMode/S07-B09_MG_RoutineSignalsSurvival_v1.mp4", 0, 4.61),
    ]),
    "S08": dict(folder="S08_Blueprint", voice="04_audio/S08_Beth_TestRead.mp3", segs=[
        ("mg", "S08_Blueprint/S08-B01_MG_FlipTheScript_v1.mp4", 0, 4.42),
        ("mg", "S08_Blueprint/S08-B02_MG_BlueprintOverview_v1.mp4", 0, 9.19),
        ("mg", "S08_Blueprint/S08-B03_MG_Step1PhoneOff_v1.mp4", 0, 10.20),
        ("mg", "S08_Blueprint/S08-B04_MG_Step2Hydrate_v1.mp4", 0, 9.61),
        ("3d", "S08_Blueprint/S08-B05_3D_HydratedBlood_v1.mp4", 1.6, 4.83, "S08-B05_3D_HydratedBlood — water floods in, cells plump up"),
        ("mg", "S08_Blueprint/S08-B06_MG_Step3Sunlight_v1.mp4", 0, 7.30),
        ("host", None, 0, 7.09, "S08-B07 · \"This sets your master circadian clock…\""),
        ("mg", "S08_Blueprint/S08-B08_MG_Step4Walk_v1.mp4", 0, 4.74),
        ("3d", "S08_Blueprint/S08-B09_3D_SunriseWalk_v1.mp4", 1.0, 4.49, "S08-B09_3D_SunriseWalk — brain & muscle walk at sunrise"),
        ("mg", "S08_Blueprint/S08-B10_MG_Step5CoffeeLater_v1.mp4", 0, 7.92),
        ("mg", "S08_Blueprint/S08-B11_MG_SmoothEnergy_v1.mp4", 0, 7.12),
        ("mg", "S08_Blueprint/S08-B12_MG_Step6ProteinFirst_v1.mp4", 0, 9.76),
        ("host", None, 0, 2.93, "S08-B13 · \"…quiets brain craving signals for hours.\""),
        ("mg", "S08_Blueprint/S08-B14_MG_Step7Calm_v1.mp4", 0, 4.07),
        ("mg", "S08_Blueprint/S08-B15_MG_Breathing_v1.mp4", 0, 4.55),
        ("3d", "S08_Blueprint/S08-B16_3D_BrainCalm_v1.mp4", 1.0, 4.51, "S08-B16_3D_BrainCalm — brain meditates, alarms fade"),
    ]),
    "S09": dict(folder="S09_Outro", voice="04_audio/S09_Beth_TestRead.mp3", segs=[
        ("host", None, 0, 3.73, "S09-B01 · \"Your metabolism isn't broken…\""),
        ("mg", "S09_Outro/S09-B02_MG_ChangeTheSignals_v1.mp4", 0, 8.69),
        ("mg", "S09_Outro/S09-B03_MG_FatBurningOn_v1.mp4", 0, 2.97),
        ("host", None, 0, 6.39, "S09-B04 · \"Pick just two or three of these steps…\""),
    ]),
}


def placeholder(label, kind, out):
    bg = "background:url(../host_ref.jpg) center/cover;" if kind == "host" else "background:radial-gradient(circle at 50% 45%, #6b2a3a, #2a0a18 70%);"
    head = "HOST ON CAMERA" if kind == "host" else "3D · GOOGLE FLOW"
    html = ROOT / "ph" / (out.stem + ".html")
    html.write_text(f"""<!doctype html><html><head><meta charset=utf-8><link rel=stylesheet href="../theme.css"></head>
<body><div id=stage style="{bg}"><div class="layer" style="background:rgba(0,0,0,.25)"></div>
<div class="abs" style="left:60px;bottom:60px;padding:24px 40px;border-radius:24px;background:rgba(10,5,40,.8);border:3px dashed rgba(255,255,255,.5)">
<div style="font-size:54px;font-weight:700;color:#ffd166">{head} <span style="font-size:32px;color:#fff;opacity:.7">(placeholder)</span></div>
<div style="font-size:36px;margin-top:8px;font-family:Nunito;font-weight:700">{label}</div></div></div>
<script>window.CLIP={{duration:1,render(){{}}}}</script></body></html>""")
    subprocess.run(["node", str(ROOT / "render.js"), str(html), str(out.with_suffix("")), "30", "--preview", "0"], check=True)
    Path(str(out.with_suffix("")) + "_t0.00.png").rename(out)


def build(sec):
    S = SECTIONS[sec]
    ins, vf, af, vlabels, alabels = [], [], [], [], []
    for i, seg in enumerate(S["segs"]):
        kind, src, cin, dur = seg[:4]
        label = seg[4] if len(seg) > 4 else ""
        path = G / src if src else None
        if kind == "host" or not path.exists():
            png = ROOT / "ph" / f"{sec}_{i:02d}.png"
            placeholder(label, "host" if kind == "host" else "3d", png)
            ins += ["-loop", "1", "-framerate", "30", "-t", f"{dur}", "-i", str(png)]
            vf.append(f"[{i}:v]zoompan=z='1+0.0008*on':d=1:s=1920x1080:fps=30,trim=duration={dur},setpts=PTS-STARTPTS[v{i}]")
            af.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={dur}[a{i}]")
        else:
            ins += ["-i", str(path)]
            vf.append(f"[{i}:v]trim=start={cin}:duration={dur},setpts=PTS-STARTPTS,fps=30,scale=1920:1080[v{i}]")
            if kind == "mg":
                af.append(f"[{i}:a]atrim=start={cin}:duration={dur},asetpts=PTS-STARTPTS[a{i}]")
            else:
                af.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={dur}[a{i}]")
        vlabels.append(f"[v{i}]"); alabels.append(f"[a{i}]")
    n = len(S["segs"])
    ins += ["-i", str(PROJ / S["voice"])]
    fc = ";".join(vf + af) + f";{''.join(vlabels)}concat=n={n}:v=1:a=0,format=yuv420p[v];" \
         f"{''.join(alabels)}concat=n={n}:v=0:a=1,volume=0.55[sfx];[{n}:a]aresample=48000,aformat=channel_layouts=stereo[vo];" \
         f"[vo][sfx]amix=inputs=2:duration=first:normalize=0[a]"
    out = G / S["folder"] / f"{sec}_PREVIEW_Animatic_WithVoice_v1.mp4"
    k = 1
    while out.exists():
        k += 1; out = out.with_name(f"{sec}_PREVIEW_Animatic_WithVoice_v{k}.mp4")
    subprocess.run([FF, "-y", "-loglevel", "error", *ins, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)], check=True)
    print("→", out)


if __name__ == "__main__":
    build(sys.argv[1])
