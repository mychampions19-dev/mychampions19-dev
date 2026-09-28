// Offline renderer: drives index.html in headless Chromium, one deterministic frame at a time.
//   node render.mjs timeline               -> out/timeline.json (cue list for audio.py)
//   node render.mjs stills 4.5 12 30 ...    -> out/still-<t>.png
//   node render.mjs video                   -> out/frames.mp4 (silent H.264, 1920x1080 @ 24 fps)
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const out = resolve(here, 'out');
mkdirSync(out, { recursive: true });
const page_url = pathToFileURL(resolve(here, '..', 'index.html')).href + '?render=1';
const ffmpeg = process.env.FFMPEG || 'ffmpeg';
const [mode = 'video', ...args] = process.argv.slice(2);

const browser = await chromium.launch({
  executablePath: process.env.CHROMIUM || undefined,
  args: ['--force-color-profile=srgb', '--disable-gpu-vsync'],
});
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
await page.goto(page_url);
await page.waitForFunction(() => typeof window.renderAt === 'function');
const clip = { x: 0, y: 0, width: 1920, height: 1080 };

if (mode === 'timeline') {
  const tl = await page.evaluate(() => window.TIMELINE);
  writeFileSync(resolve(out, 'timeline.json'), JSON.stringify(tl, null, 1));
  console.log('wrote timeline.json:', tl.captions.length, 'captions,', tl.sfx.length, 'sfx,', tl.music.length, 'notes');
} else if (mode === 'stills') {
  for (const t of args.map(Number)) {
    await page.evaluate(t => window.renderAt(t), t);
    await page.screenshot({ path: resolve(out, `still-${t.toFixed(2)}.png`), clip });
  }
  console.log('stills:', args.join(' '));
} else {
  const { fps, duration } = await page.evaluate(() => window.TIMELINE);
  const n = Math.round(fps * duration);
  const enc = spawn(ffmpeg, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', String(fps), resolve(out, 'frames.mp4')],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let f = 0; f < n; f++) {
    await page.evaluate(t => window.renderAt(t), f / fps);
    const buf = await page.screenshot({ type: 'jpeg', quality: 95, clip });
    if (!enc.stdin.write(buf)) await new Promise(r => enc.stdin.once('drain', r));
    if (f % 120 === 0) console.log(`frame ${f}/${n}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  enc.stdin.end();
  await new Promise((r, j) => enc.on('close', c => c === 0 ? r() : j(new Error('ffmpeg exited ' + c))));
  console.log(`frames.mp4: ${n} frames in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
}
await browser.close();
