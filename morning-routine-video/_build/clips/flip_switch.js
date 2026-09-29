// Glass body with belly switch that flips STORE → BURN (callback to S01-B02). window.FS = {flipAt, title, tag, sunrise}
(function () {
  const C = window.FS;
  const st = $('#stage');
  if (C.sunrise) st.style.background = 'linear-gradient(160deg, #2a1250 0%, #6b2a6a 45%, #ff8a5c 100%)';
  st.insertAdjacentHTML('beforeend', `
  <style>
    #fsWrap { left:960px; top:150px; width:600px; height:900px; margin-left:-300px; transform-origin:50% 0; }
    #fsWrap svg { position:absolute; inset:0; overflow:visible; }
    #fsSw { position:absolute; left:190px; top:350px; width:220px; height:104px; border-radius:52px; transform: scale(1.35);
      background:#120a36; box-shadow: inset 0 6px 14px rgba(0,0,0,.7), 0 0 0 6px rgba(255,255,255,.25), 0 0 60px var(--glow); }
    #fsTrack { position:absolute; inset:8px; border-radius:44px; }
    #fsKnob { position:absolute; top:10px; width:84px; height:84px; --c1:#fff; --c2:#bdb6e8; }
    .fsL { position:absolute; top:34px; font:700 30px 'Fredoka'; }
    #fsTitle { left:50%; top:60px; font-size:104px; }
    #fsTag { left:960px; top:960px; white-space:nowrap; }
    #fsFlash { position:absolute; inset:0; background:radial-gradient(circle at 50% 50%, rgba(255,177,59,.9), rgba(255,90,54,0) 60%); opacity:0; }
  </style>
  <div id="fsFlash"></div>
  <div id="fsWrap" class="abs"><svg viewBox="0 0 600 900">
    <defs><radialGradient id="fsG" cx="50%" cy="45%" r="50%"><stop offset="0" id="fsG0" stop-color="#5b6bff" stop-opacity=".75"/><stop offset="1" stop-color="#5b6bff" stop-opacity="0"/></radialGradient>
      <linearGradient id="fsGl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a2a8a"/><stop offset="1" stop-color="#170d47"/></linearGradient></defs>
    <g id="fsOut" stroke-linecap="round"><circle cx="300" cy="105" r="92"/><rect x="160" y="195" width="280" height="370" rx="120"/>
      <line x1="185" y1="260" x2="90" y2="540" stroke-width="98"/><line x1="415" y1="260" x2="510" y2="540" stroke-width="98"/>
      <line x1="240" y1="520" x2="222" y2="850" stroke-width="112"/><line x1="360" y1="520" x2="378" y2="850" stroke-width="112"/></g>
    <g fill="url(#fsGl)" stroke="url(#fsGl)" stroke-linecap="round"><circle cx="300" cy="105" r="80"/><rect x="172" y="207" width="256" height="346" rx="110"/>
      <line x1="185" y1="260" x2="90" y2="540" stroke-width="74"/><line x1="415" y1="260" x2="510" y2="540" stroke-width="74"/>
      <line x1="240" y1="520" x2="222" y2="850" stroke-width="88"/><line x1="360" y1="520" x2="378" y2="850" stroke-width="88"/></g>
    <ellipse cx="300" cy="400" rx="200" ry="200" fill="url(#fsG)"/><ellipse cx="250" cy="70" rx="30" ry="18" fill="rgba(255,255,255,.35)"/>
  </svg>
  <div id="fsSw"><div id="fsTrack"></div><div class="fsL" id="fsLS" style="left:22px;color:#bfd0ff">STORE</div><div class="fsL" id="fsLB" style="right:26px;color:#ffe2b8">BURN</div><div id="fsKnob" class="glossy"></div></div></div>
  <div id="fsTitle" class="abs h3d burn">${C.title}</div>
  <div id="fsTag" class="abs"><span class="pill" style="font-size:64px;background:linear-gradient(135deg,#ff5a36,#ffb13b);color:#3a1400"><span class="emoji">🔥</span> ${C.tag}</span></div>`);
  window.fsRender = function (t) {
    const bp = ease.back(prog(t, .05, .6));
    $('#fsWrap').style.transform = `translateY(${lerp(900, 0, bp)}px) scale(.9)`;
    const f = ease.out(prog(t, C.flipAt, .16));
    $('#fsKnob').style.left = lerp(126, 10, f) + 'px';
    $('#fsTrack').style.background = f < .5 ? 'linear-gradient(90deg, rgba(61,107,255,.55), rgba(155,92,255,0))' : 'linear-gradient(90deg, rgba(255,90,54,0), rgba(255,177,59,.6))';
    $('#fsLS').style.opacity = f < .5 ? .95 : 0; $('#fsLB').style.opacity = f < .5 ? 0 : .95;
    const col = f < .5 ? '#7a6bff' : '#ff7a3d';
    $('#fsOut').setAttribute('stroke', col); $('#fsOut').setAttribute('fill', col);
    $('#fsG0').setAttribute('stop-color', f < .5 ? '#5b6bff' : '#ff7a3d');
    $('#fsSw').style.setProperty('--glow', f < .5 ? 'rgba(110,100,255,.9)' : 'rgba(255,140,60,.95)');
    $('#fsFlash').style.opacity = t > C.flipAt ? Math.max(0, 1 - (t - C.flipAt) / .7) : 0;
    css($('#fsTitle'), { transform: `translate(-50%,0) scale(${pop(t, C.flipAt + .1, .45)})`, opacity: t > C.flipAt + .1 ? 1 : 0 });
    css($('#fsTag'), { transform: `translate(-50%,-50%) scale(${pop(t, C.flipAt + .35, .45)})`, opacity: t > C.flipAt + .35 ? 1 : 0 });
    const sk = t > C.flipAt && t < C.flipAt + .35 ? Math.sin(t * 110) * 10 * (1 - prog(t, C.flipAt, .35)) : 0;
    $('#stage').style.transform += ` translate(${sk}px,0)`;
  };
  window.fsSfx = [[0, 'whoosh', {dur: .5}], [Math.max(0, C.flipAt - .9), 'riser', {dur: .9, vol: .18}], [C.flipAt, 'clunk', {vol: .85}], [C.flipAt, 'impact', {vol: .5}],
    [C.flipAt + .05, 'sizzle', {dur: 1.6, vol: .12}], [C.flipAt + .1, 'pop', {freq: 600}], [C.flipAt + .35, 'ding', {freq: 1319, dur: 1.2, vol: .28}]];
})();
