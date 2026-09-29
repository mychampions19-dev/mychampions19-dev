"""Render clips → mix SFX → mux final MP4s.
Usage: python3 build.py S01-B02 [S01-B04 ...]   (clip ids; names come from CLIPS below)"""
import json, subprocess, sys
from pathlib import Path
import sfx

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "03_graphics"
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"

# clip id -> (section folder, final file name)
CLIPS = {
    "S01-B02": ("S01_MetabolicSwitch", "S01-B02_MG_9AMSwitch_v1"),
    "S01-B04": ("S01_MetabolicSwitch", "S01-B04_MG_ZeroCalories_v2"),
    "S01-B06": ("S01_MetabolicSwitch", "S01-B06_MG_BurnVsStore_v2"),
    "S01-B07": ("S01_MetabolicSwitch", "S01-B07_MG_7MistakesPreview_v1"),
    "S02-B01": ("S02_Phone", "S02-B01_MG_Mistake1Title_v1"),
    "S02-B03": ("S02_Phone", "S02-B03_MG_NotificationStorm_v1"),
    "S02-B05": ("S02_Phone", "S02-B05_MG_CortisolCurve_v1"),
    "S02-B07": ("S02_Phone", "S02-B07_MG_StressSurge_v1"),
    "S02-B08": ("S02_Phone", "S02-B08_MG_StudyPNASNexus_v1"),
    "S02-B10": ("S02_Phone", "S02-B10_MG_TenYearsYounger_v1"),
    "S02-B12": ("S02_Phone", "S02-B12_MG_SurvivalVsFatBurn_v1"),
    "S02-B14": ("S02_Phone", "S02-B14_MG_3xReceptors_v1"),
    "S03-B01": ("S03_Caffeine", "S03-B01_MG_Mistake2Title_v1"),
    "S03-B02": ("S03_Caffeine", "S03-B02_MG_OvernightDehydration_v1"),
    "S03-B05": ("S03_Caffeine", "S03-B05_MG_CaffeineStressedSystem_v1"),
    "S03-B07": ("S03_Caffeine", "S03-B07_MG_JitteryCrash_v1"),
    "S03-B09": ("S03_Caffeine", "S03-B09_MG_HungerMask_v1"),
    "S03-B10": ("S03_Caffeine", "S03-B10_MG_HydrateFirst_v1"),
    "S04-B01": ("S04_MorningLight", "S04-B01_MG_Mistake3Title_v1"),
    "S04-B03": ("S04_MorningLight", "S04-B03_MG_CircadianClock_v1"),
    "S04-B04": ("S04_MorningLight", "S04-B04_MG_OutOfSync_v1"),
    "S04-B07": ("S04_MorningLight", "S04-B07_MG_NoSignal_v1"),
    "S04-B08": ("S04_MorningLight", "S04-B08_MG_LightReset_v1"),
    "S05-B01": ("S05_HighCarbBreakfast", "S05-B01_MG_Mistake4Title_v1"),
    "S05-B02": ("S05_HighCarbBreakfast", "S05-B02_MG_HealthyBreakfastLineup_v1"),
    "S05-B04": ("S05_HighCarbBreakfast", "S05-B04_MG_GlucoseSurge_v1"),
    "S05-B05": ("S05_HighCarbBreakfast", "S05-B05_MG_FatBurnSuppressed_v1"),
    "S05-B06": ("S05_HighCarbBreakfast", "S05-B06_MG_SugarCrash_v1"),
    "S05-B07": ("S05_HighCarbBreakfast", "S05-B07_MG_CrashSymptoms_v1"),
    "S05-B10": ("S05_HighCarbBreakfast", "S05-B10_MG_fMRICravingsStudy_v1"),
    "S05-B11": ("S05_HighCarbBreakfast", "S05-B11_MG_EggsVsBagel_v1"),
}


def build(cid):
    folder, name = CLIPS[cid]
    tmp = ROOT / "tmp"; tmp.mkdir(exist_ok=True)
    base = tmp / name
    subprocess.run(["node", str(ROOT / "render.js"), str(ROOT / "clips" / f"{cid}.html"), str(base)], check=True)
    meta = json.loads((base.with_suffix(".sfx.json")).read_text())
    events = [(t, getattr(sfx, kind)(**(kw or {}))) for t, kind, *rest in meta["sfx"] for kw in [rest[0] if rest else None]]
    wav = base.with_suffix(".wav")
    sfx.write_wav(wav, sfx.mix(events, meta["duration"]))
    dest = OUT / folder; dest.mkdir(parents=True, exist_ok=True)
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", str(base) + ".video.mp4", "-i", str(wav),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                    str(dest / f"{name}.mp4")], check=True)
    print("→", dest / f"{name}.mp4")


if __name__ == "__main__":
    for c in sys.argv[1:] or CLIPS:
        build(c)
