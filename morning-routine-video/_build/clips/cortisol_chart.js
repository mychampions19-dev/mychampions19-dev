// Shared cortisol-after-waking chart used by S02-B05 and S02-B07 (identical framing so the cut between them is seamless)
const CH = { x0: 300, x1: 1680, y0: 880, y1: 300, mMax: 90 };
const X = m => CH.x0 + (m / CH.mMax) * (CH.x1 - CH.x0);
const Y = v => CH.y0 - v * (CH.y0 - CH.y1);
const natural = m => .22 + .52 * Math.exp(-Math.pow((m - 37) / 15, 2)) + .08 * (1 - Math.exp(-m / 10));
function pathOf(fn, mEnd, step = 1) {
  let d = '';
  for (let m = 0; m <= mEnd + 1e-6; m += step) d += (m ? 'L' : 'M') + X(m).toFixed(1) + ' ' + Y(fn(m)).toFixed(1) + ' ';
  return d;
}
function areaOf(fn, mEnd, step = 1) {
  return pathOf(fn, mEnd, step) + `L${X(mEnd).toFixed(1)} ${CH.y0} L${X(0)} ${CH.y0} Z`;
}
function buildChart(stage) {
  const ticks = [0, 15, 30, 45, 60, 75, 90].map(m => `
    <line x1="${X(m)}" y1="${CH.y0}" x2="${X(m)}" y2="${CH.y0 + 14}" stroke="rgba(255,255,255,.5)" stroke-width="4"/>
    <text x="${X(m)}" y="${CH.y0 + 58}" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="36" fill="rgba(255,255,255,.75)">${m}</text>`).join('');
  const grid = [.25, .5, .75, 1].map(v => `<line x1="${CH.x0}" y1="${Y(v)}" x2="${CH.x1}" y2="${Y(v)}" stroke="rgba(255,255,255,.08)" stroke-width="3"/>`).join('');
  (stage.querySelector('#cells') ? stage.querySelector('#cells') : stage).insertAdjacentHTML(stage.querySelector('#cells') ? 'afterend' : 'beforeend', `
  <svg id="chart" class="layer" viewBox="0 0 1920 1080" style="overflow:visible">
    <defs>
      <linearGradient id="natG" x1="0" x2="1"><stop offset="0" stop-color="#2ee6a8"/><stop offset=".45" stop-color="#ffd166"/><stop offset="1" stop-color="#2ee6a8"/></linearGradient>
      <linearGradient id="natA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2ee6a8" stop-opacity=".45"/><stop offset="1" stop-color="#2ee6a8" stop-opacity="0"/></linearGradient>
      <linearGradient id="strA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff3b5c" stop-opacity=".85"/><stop offset="1" stop-color="#ff3b5c" stop-opacity=".2"/></linearGradient>
      <clipPath id="revealClip"><rect id="revealRect" x="0" y="0" width="0" height="1080"/></clipPath>
    </defs>
    <g id="axes">
      ${grid}
      <rect id="band" x="${X(30)}" y="${CH.y1 - 40}" width="${X(45) - X(30)}" height="${CH.y0 - CH.y1 + 40}" rx="18" fill="rgba(255,209,102,.16)" stroke="rgba(255,209,102,.6)" stroke-width="3" stroke-dasharray="12 10"/>
      <line x1="${CH.x0}" y1="${CH.y0}" x2="${CH.x1 + 30}" y2="${CH.y0}" stroke="rgba(255,255,255,.7)" stroke-width="6" stroke-linecap="round"/>
      <line x1="${CH.x0}" y1="${CH.y0}" x2="${CH.x0}" y2="${CH.y1 - 60}" stroke="rgba(255,255,255,.7)" stroke-width="6" stroke-linecap="round"/>
      ${ticks}
      <text x="${(CH.x0 + CH.x1) / 2}" y="${CH.y0 + 120}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="40" fill="#fff" letter-spacing="3">MINUTES AFTER WAKING</text>
      <text x="${CH.x0 - 40}" y="${(CH.y0 + CH.y1) / 2}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="40" fill="#fff" letter-spacing="3" transform="rotate(-90 ${CH.x0 - 40} ${(CH.y0 + CH.y1) / 2})">CORTISOL</text>
    </g>
    <path id="flood" d="" fill="url(#strA)"/>
    <path id="strArea" d="" fill="url(#strA)"/>
    <path id="strLine" d="" fill="none" stroke="#ff3b5c" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 0 14px #ff3b5c)"/>
    <g clip-path="url(#revealClip)">
      <path id="natArea" d="${areaOf(natural, 90)}" fill="url(#natA)"/>
      <path id="natLine" d="${pathOf(natural, 90)}" fill="none" stroke="url(#natG)" stroke-width="12" stroke-linecap="round" style="filter:drop-shadow(0 0 12px rgba(46,230,168,.8))"/>
    </g>
    <circle id="head" r="18" fill="#fff" style="filter:drop-shadow(0 0 16px #fff)"/>
  </svg>`);
}
