#!/usr/bin/env bash
# Full pipeline: picture -> cue list -> soundtrack -> mux.
# Needs: node + playwright (Chromium), python3 + numpy, espeak-ng + mbrola-en1, ffmpeg.
set -euo pipefail
cd "$(dirname "$0")"
node render.mjs timeline
node render.mjs video
python3 audio.py
./mux.sh
