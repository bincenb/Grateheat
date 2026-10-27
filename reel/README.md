# GrateHeat Instagram reel

`grateheat_reel.mp4` is a 24-second vertical reel (1080×1920, 30 fps) made from the site's own 3D models, school map data and energy model numbers. The beat and sound effects are synthesized in `audio.py`, so the reel has no licensed music. `CAPTION.md` has a ready-to-post caption, hashtags and posting tips.

## Rebuild it

From the repository root:

```
python3 -m http.server 8765 &
cd reel
node render.js test         # a few still frames into reel/test/
node render.js full         # video.mp4 (needs Playwright + ffmpeg)
python3 audio.py            # audio.wav
ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac -b:a 256k -movflags +faststart -shortest grateheat_reel.mp4
```

The timeline lives in `renderAt(t)` in `reel.html`, and the sound effect cue times at the bottom of `audio.py` match its scene changes.
