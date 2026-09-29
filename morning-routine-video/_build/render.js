// Usage: node render.js clips/S01-B02.html out_basename [fps] [--preview t1,t2,...]
// Renders an HTML clip frame-by-frame to an H.264 MP4 (silent) + writes its SFX cue list as JSON.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const FFMPEG = '/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2';
const [clip, outBase, fpsArg, flag, stills] = process.argv.slice(2);
const fps = +(fpsArg || 30);

(async () => {
  const browser = await chromium.launch({ args: ['--font-render-hinting=none', '--disable-gpu-vsync'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', e => { console.error('PAGE ERROR', e.message); process.exit(1); });
  await page.goto('file://' + path.resolve(clip));
  await page.evaluate(() => document.fonts.ready);
  const { duration, sfx } = await page.evaluate(() => ({ duration: CLIP.duration, sfx: CLIP.sfx || [] }));

  if (flag === '--preview') {
    for (const t of stills.split(',').map(Number)) {
      await page.evaluate(t => CLIP.render(t), t);
      await page.screenshot({ path: `${outBase}_t${t.toFixed(2)}.png` });
    }
    await browser.close();
    return;
  }

  fs.writeFileSync(outBase + '.sfx.json', JSON.stringify({ duration, sfx }));
  const ff = spawn(FFMPEG, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', String(fps),
    outBase + '.video.mp4'], { stdio: ['pipe', 'inherit', 'inherit'] });
  const n = Math.round(duration * fps);
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => CLIP.render(t), i / fps);
    const buf = await page.screenshot({ type: 'png' });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 30 === 0) process.stdout.write(`\r${path.basename(outBase)} ${i}/${n}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  console.log(`\r${path.basename(outBase)} done (${n} frames)`);
  await browser.close();
})();
