// Deterministic animation helpers. Every clip defines window.CLIP = {duration, render(t)}
// and the renderer calls render(t) once per frame — no CSS animations, so output is frame-exact.
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, p) => a + (b - a) * p;
const prog = (t, start, dur) => clamp((t - start) / dur);
const ease = {
  out: p => 1 - Math.pow(1 - p, 3),
  in: p => p * p * p,
  inOut: p => (p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2),
  back: p => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2); },
  elastic: p => p === 0 || p === 1 ? p : Math.pow(2, -10 * p) * Math.sin((p * 10 - .75) * (2 * Math.PI) / 3) + 1,
};
// Pop-in: 0 → overshoot → 1
const pop = (t, start, dur = .45) => ease.back(prog(t, start, dur));
const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];
function el(tag, cls, parent, html) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (html !== undefined) e.innerHTML = html;
  (parent || document.getElementById('stage')).appendChild(e);
  return e;
}
function css(e, o) { for (const k in o) e.style[k] = o[k]; }
// Seeded random so particles are identical every render
function rand(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }

// Ambient floating cells behind everything. palette = array of [c1,c2].
function makeCells(n, palette, seed = 1, parent) {
  const r = rand(seed), host = parent || el('div', 'layer');
  const cells = [];
  for (let i = 0; i < n; i++) {
    const size = 20 + r() * 140, depth = .3 + r() * .7;
    const [c1, c2] = palette[Math.floor(r() * palette.length)];
    const c = el('div', 'cell', host);
    css(c, { width: size + 'px', height: size + 'px',
      background: `radial-gradient(circle at 35% 30%, ${c1}, ${c2} 70%)`,
      opacity: (.12 + depth * .25).toFixed(2), filter: `blur(${((1 - depth) * 8).toFixed(1)}px)` });
    cells.push({ c, x: r() * 2100 - 90, y: r() * 1200 - 60, vx: (r() - .5) * 40 * depth, vy: -(10 + r() * 40) * depth,
      wob: r() * 6.28, size });
  }
  return {
    host,
    update(t) {
      for (const p of cells) {
        const x = p.x + p.vx * t + Math.sin(t * .8 + p.wob) * 12;
        let y = (p.y + p.vy * t) % 1260; if (y < -150) y += 1260;
        p.c.style.transform = `translate(${x}px, ${y}px)`;
      }
    },
  };
}

// Clip-level entry punch (first ~0.25s): slight zoom-settle so the cut from the host feels energetic
function entryPunch(t) {
  const p = ease.out(prog(t, 0, .35));
  $('#stage').style.transform = `scale(${lerp(1.06, 1, p)})`;
  $('#stage').style.filter = p < 1 ? `blur(${lerp(6, 0, p).toFixed(2)}px) brightness(${lerp(1.5, 1, p).toFixed(2)})` : 'none';
}
