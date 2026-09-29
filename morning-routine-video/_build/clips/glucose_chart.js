// Shared blood-sugar / insulin chart for S05-B04 and S05-B06 (identical framing)
const GC = { x0: 300, x1: 1680, y0: 860, y1: 300, mMax: 180, base: .4 };
const GX = m => GC.x0 + m / GC.mMax * (GC.x1 - GC.x0);
const GY = v => GC.y0 - v * (GC.y0 - GC.y1);
const glucose = m => GC.base + .5 * Math.exp(-Math.pow((m - 32) / 16, 2)) - .2 * Math.exp(-Math.pow((m - 105) / 20, 2)) * (m > 60 ? 1 : 0);
const insulin = m => .08 + .75 * Math.exp(-Math.pow((m - 55) / 24, 2));
function gPath(fn, m0, m1) { let d = ''; for (let m = m0; m <= m1 + 1e-6; m += 1) d += (m === m0 ? 'M' : 'L') + GX(m).toFixed(1) + ' ' + GY(fn(m)).toFixed(1) + ' '; return d; }
function gArea(fn, m0, m1) { return gPath(fn, m0, m1) + `L${GX(m1)} ${GC.y0} L${GX(m0)} ${GC.y0} Z`; }
function buildGlucoseChart(stage) {
  stage.querySelector('#cells').insertAdjacentHTML('afterend', `
  <svg id="gchart" class="layer" viewBox="0 0 1920 1080" style="overflow:visible">
    <defs>
      <linearGradient id="insA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3d6bff" stop-opacity=".55"/><stop offset="1" stop-color="#3d6bff" stop-opacity="0"/></linearGradient>
      <linearGradient id="gluL" x1="0" x2="1"><stop offset="0" stop-color="#2ee6a8"/><stop offset=".25" stop-color="#ffb13b"/><stop offset=".5" stop-color="#ff5a36"/><stop offset=".75" stop-color="#ff3b5c"/><stop offset="1" stop-color="#2ee6a8"/></linearGradient>
      <clipPath id="gReveal"><rect id="gRevealR" x="0" y="0" width="0" height="1080"/></clipPath>
      <clipPath id="iReveal"><rect id="iRevealR" x="0" y="0" width="0" height="1080"/></clipPath>
    </defs>
    <rect id="lowZone" x="${GC.x0}" y="${GY(GC.base)}" width="${GC.x1 - GC.x0}" height="${GC.y0 - GY(GC.base)}" fill="rgba(255,59,92,.12)" opacity="0"/>
    <line x1="${GC.x0}" y1="${GC.y0}" x2="${GC.x1 + 30}" y2="${GC.y0}" stroke="rgba(255,255,255,.7)" stroke-width="6" stroke-linecap="round"/>
    <line x1="${GC.x0}" y1="${GC.y0}" x2="${GC.x0}" y2="${GC.y1 - 60}" stroke="rgba(255,255,255,.7)" stroke-width="6" stroke-linecap="round"/>
    <line x1="${GC.x0}" y1="${GY(GC.base)}" x2="${GC.x1}" y2="${GY(GC.base)}" stroke="rgba(255,255,255,.35)" stroke-width="4" stroke-dasharray="16 12"/>
    <text x="${GC.x1 + 10}" y="${GY(GC.base) + 12}" font-family="Fredoka" font-weight="600" font-size="32" fill="rgba(255,255,255,.6)">baseline</text>
    <text x="${(GC.x0 + GC.x1) / 2}" y="${GC.y0 + 70}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="40" fill="#fff" letter-spacing="3">TIME AFTER BREAKFAST</text>
    <text x="${GC.x0 - 40}" y="${(GC.y0 + GC.y1) / 2}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="40" fill="#fff" letter-spacing="3" transform="rotate(-90 ${GC.x0 - 40} ${(GC.y0 + GC.y1) / 2})">BLOOD SUGAR</text>
    <g clip-path="url(#iReveal)"><path d="${gArea(insulin, 0, 180)}" fill="url(#insA)"/><path d="${gPath(insulin, 0, 180)}" fill="none" stroke="#7f9bff" stroke-width="8" stroke-dasharray="18 12"/></g>
    <g clip-path="url(#gReveal)"><path id="gLine" d="${gPath(glucose, 0, 180)}" fill="none" stroke="url(#gluL)" stroke-width="14" stroke-linecap="round" style="filter:drop-shadow(0 0 12px rgba(255,120,60,.8))"/></g>
    <circle id="gHead" r="18" fill="#fff" style="filter:drop-shadow(0 0 14px #fff)"/>
  </svg>`);
}
function revealGlucose(mNow) { $('#gRevealR').setAttribute('width', GX(mNow) + 8); $('#gHead').setAttribute('cx', GX(mNow)); $('#gHead').setAttribute('cy', GY(glucose(mNow))); }
function revealInsulin(mNow) { $('#iRevealR').setAttribute('width', GX(mNow) + 4); }
