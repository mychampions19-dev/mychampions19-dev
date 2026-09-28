#!/usr/bin/env bash
# Mux the picture with the soundtrack and a soft caption track.
# Captions are also burned into the terminal caption bar, so either works.
set -euo pipefail
cd "$(dirname "$0")/out"
FF="${FFMPEG:-ffmpeg}"
# Delivery encode: the paper grain re-rolls 8x a second, so tune for animation at CRF 25 (~25 MB).
"$FF" -y -loglevel error -i frames.mp4 -c:v libx264 -preset slow -crf 25 -tune animation -pix_fmt yuv420p video.mp4
mux() {  # $1 audio wav, $2 output
  "$FF" -y -loglevel error -i video.mp4 -i "$1" -i captions.srt \
    -map 0:v -map 1:a -map 2:s -c:v copy -c:a aac -b:a 192k -c:s mov_text \
    -metadata:s:s:0 language=eng -metadata title="Why Is the Sky Blue?" -movflags +faststart "$2"
}
mux mix.wav      sky-is-blue.mp4           # music + SFX + scratch voiceover
mux music_fx.wav sky-is-blue_music-fx.mp4  # M&E: no voice, for a real VO record
ls -lh sky-is-blue*.mp4
