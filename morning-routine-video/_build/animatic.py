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
    "S02": dict(folder="S02_Phone", voice="04_audio/S02_Beth_TestRead.mp3", segs=[
        ("mg", "S02_Phone/S02-B01_MG_Mistake1Title_v1.mp4", 0, 4.93),
        ("3d", "S02_Phone/S02-B02_3D_PhoneAlarmWake_v1.mp4", 1.0, 4.81, "S02-B02_3D_PhoneAlarmWake — brain grabs the buzzing phone"),
        ("mg", "S02_Phone/S02-B03_MG_NotificationStorm_v1.mp4", 0, 5.97),
        ("host", None, 0, 1.91, "S02-B04 · \"Here's why that's a biological problem.\""),
        ("mg", "S02_Phone/S02-B05_MG_CortisolCurve_v1.mp4", 0, 8.07),
        ("3d", "S02_Phone/S02-B06_3D_BrainEngineStart_v1.mp4", 2.0, 2.03, "S02-B06_3D_BrainEngineStart — brain turns the ignition key"),
        ("mg", "S02_Phone/S02-B07_MG_StressSurge_v1.mp4", 0, 8.61),
        ("mg", "S02_Phone/S02-B08_MG_StudyPNASNexus_v1.mp4", 0, 10.47),
        ("host", None, 0, 6.19, "S02-B09 · \"In just 14 days…\""),
        ("mg", "S02_Phone/S02-B10_MG_TenYearsYounger_v1.mp4", 0, 5.24),
        ("host", None, 0, 6.17, "S02-B11 · \"When you flood your system…\""),
        ("mg", "S02_Phone/S02-B12_MG_SurvivalVsFatBurn_v1.mp4", 0, 2.74),
        ("3d", "S01_MetabolicSwitch/S01-B03_3D_VisceralFatHug_v1.mp4", 4.6, 3.34, "reused S01-B03"),
        ("mg", "S02_Phone/S02-B14_MG_3xReceptors_v1.mp4", 0, 3.73),
        ("3d", "S02_Phone/S02-B15_3D_CortisolDirectsFat_v1.mp4", 1.0, 3.9, "S02-B15_3D_CortisolDirectsFat — gremlin marshals direct fat to the belly"),
    ]),
    "S03": dict(folder="S03_Caffeine", voice="04_audio/S03_Beth_TestRead.mp3", segs=[
        ("mg", "S03_Caffeine/S03-B01_MG_Mistake2Title_v1.mp4", 0, 3.01),
        ("mg", "S03_Caffeine/S03-B02_MG_OvernightDehydration_v1.mp4", 0, 7.00),
        ("3d", "S03_Caffeine/S03-B03_3D_DehydratedBlood_v1.mp4", 1.0, 5.39, "S03-B03_3D_DehydratedBlood — crowded, sluggish blood cells"),
        ("host", None, 0, 1.97, "S03-B04 · \"So what do most people reach for first?\""),
        ("mg", "S03_Caffeine/S03-B05_MG_CaffeineStressedSystem_v1.mp4", 0, 5.68),
        ("3d", "S03_Caffeine/S03-B06_3D_GasolineOnFire_v1.mp4", 2.0, 4.20, "S03-B06_3D_GasolineOnFire — coffee cup pours onto the gremlin's fire"),
        ("mg", "S03_Caffeine/S03-B07_MG_JitteryCrash_v1.mp4", 0, 3.30),
        ("host", None, 0, 1.85, "S03-B08 · \"Here's a key metabolic insight:\""),
        ("mg", "S03_Caffeine/S03-B09_MG_HungerMask_v1.mp4", 0, 7.29),
        ("mg", "S03_Caffeine/S03-B10_MG_HydrateFirst_v1.mp4", 0, 6.01),
    ]),
    "S04": dict(folder="S04_MorningLight", voice="04_audio/S04_Beth_TestRead.mp3", segs=[
        ("mg", "S04_MorningLight/S04-B01_MG_Mistake3Title_v1.mp4", 0, 5.32),
        ("3d", "S04_MorningLight/S04-B02_3D_BrainMasterClock_v1.mp4", 1.0, 3.62, "S04-B02_3D_BrainMasterClock — brain winds the giant sun & moon clock"),
        ("mg", "S04_MorningLight/S04-B03_MG_CircadianClock_v1.mp4", 0, 10.07),
        ("mg", "S04_MorningLight/S04-B04_MG_OutOfSync_v1.mp4", 0, 4.83),
        ("host", None, 0, 4.56, "S04-B05 · \"Studies link bright light early in the day…\""),
        ("3d", "S04_MorningLight/S04-B06_3D_FluorescentGloom_v1.mp4", 1.0, 3.49, "S04-B06_3D_FluorescentGloom — brain stuck under a flickering office light"),
        ("mg", "S04_MorningLight/S04-B07_MG_NoSignal_v1.mp4", 0, 3.63),
        ("mg", "S04_MorningLight/S04-B08_MG_LightReset_v1.mp4", 0, 7.81),
    ]),
    "S05": dict(folder="S05_HighCarbBreakfast", voice="04_audio/S05_Beth_TestRead.mp3", segs=[
        ("mg", "S05_HighCarbBreakfast/S05-B01_MG_Mistake4Title_v1.mp4", 0, 6.41),
        ("mg", "S05_HighCarbBreakfast/S05-B02_MG_HealthyBreakfastLineup_v1.mp4", 0, 4.33),
        ("3d", "S05_HighCarbBreakfast/S05-B03_3D_DessertInDisguise_v1.mp4", 1.0, 6.32, "S05-B03_3D_DessertInDisguise — oatmeal bowl unmasks as a cake"),
        ("mg", "S05_HighCarbBreakfast/S05-B04_MG_GlucoseSurge_v1.mp4", 0, 11.39),
        ("mg", "S05_HighCarbBreakfast/S05-B05_MG_FatBurnSuppressed_v1.mp4", 0, 3.62),
        ("mg", "S05_HighCarbBreakfast/S05-B06_MG_SugarCrash_v1.mp4", 0, 4.41),
        ("mg", "S05_HighCarbBreakfast/S05-B07_MG_CrashSymptoms_v1.mp4", 0, 5.92),
        ("3d", "S05_HighCarbBreakfast/S05-B08_3D_SugarRollercoaster_v1.mp4", 1.0, 2.79, "S05-B08_3D_SugarRollercoaster — brain on a blood sugar rollercoaster"),
        ("host", None, 0, 2.77, "S05-B09 · \"Contrast that with research from the University of Missouri.\""),
        ("mg", "S05_HighCarbBreakfast/S05-B10_MG_fMRICravingsStudy_v1.mp4", 0, 13.41),
        ("mg", "S05_HighCarbBreakfast/S05-B11_MG_EggsVsBagel_v1.mp4", 0, 9.31),
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
