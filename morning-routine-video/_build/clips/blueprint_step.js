// Reusable "STEP N" blueprint card (Section 8). Bright sunrise palette = the "fix", contrasting the dark mistake cards.
// window.BS = { n, icon, title:[line1,line2?], hit, titleAt, bullets:[{t, at, e}], duration, tile:[c1,c2], extra?:fn(t) }
(function () {
  const C = window.BS;
  const st = document.getElementById('stage');
  st.style.background = 'linear-gradient(160deg, #ff9a6b 0%, #ff6f91 38%, #8a5cff 100%)';
  st.insertAdjacentHTML('beforeend', `
  <style>
    #bsSun { position:absolute; right:-160px; top:-160px; width:640px; height:640px; border-radius:50%;
      background: radial-gradient(circle, rgba(255,240,180,.95), rgba(255,200,120,.5) 40%, rgba(255,200,120,0) 70%); }
    .bsRay { position:absolute; right:160px; top:160px; width:900px; height:26px; margin-top:-13px; transform-origin:100% 50%;
      background: linear-gradient(90deg, rgba(255,245,200,0), rgba(255,245,200,.35)); border-radius:13px; }
    #bsStep { left:250px; top:190px; white-space:nowrap; }
    #bsStep .pill { font-size:54px; background: rgba(20,10,60,.55); letter-spacing:4px; }
    #bsBadge { left:250px; top:470px; width:300px; height:300px; margin:-150px; --c1:#ffffff; --c2:#2ee6a8; }
    #bsNum { position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); font:700 200px 'Fredoka'; color:#0b5a45; }
    #bsTile { left:250px; top:790px; width:250px; height:250px; margin:-125px; border-radius:64px;
      box-shadow: inset 0 6px 0 rgba(255,255,255,.5), inset 0 -12px 0 rgba(0,0,0,.18), 0 24px 50px rgba(40,0,60,.4); }
    #bsIcon { position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); font-size:150px; }
    #bsTitle { left:520px; top:250px; width:1320px; }
    #bsTitle .ln { font-size:104px; line-height:1.12; white-space:nowrap; }
    .bsBul { position:absolute; left:540px; white-space:nowrap; }
    .bsBul .pill { font-size:50px; background: rgba(255,255,255,.95); color:#2b1d63; box-shadow: 0 14px 30px rgba(40,0,60,.35); }
    #bsDots { left:960px; top:1010px; transform:translateX(-50%); display:flex; gap:20px; }
    .bsDot { width:46px; height:46px; border-radius:50%; background:rgba(255,255,255,.3); font:700 26px 'Fredoka'; display:flex; align-items:center; justify-content:center; color:rgba(255,255,255,.8); }
    .bsDot.on { background:#2ee6a8; color:#0b5a45; box-shadow:0 0 20px #2ee6a8; }
    .bsDot.done { background:rgba(255,255,255,.75); color:#2b1d63; }
  </style>
  <div id="bsSun"></div><div id="bsRays"></div>
  <div id="bsStep" class="abs"><span class="pill">STEP</span></div>
  <div id="bsBadge" class="abs glossy"><div id="bsNum">${C.n}</div></div>
  <div id="bsTile" class="abs" style="background:linear-gradient(160deg,${C.tile[0]},${C.tile[1]})"><div id="bsIcon" class="emoji">${C.icon}</div></div>
  <div id="bsTitle" class="abs">${C.title.map(l => `<div class="ln h3d">${l}</div>`).join('')}</div>
  ${C.bullets.map((b, i) => `<div class="bsBul" id="bsB${i}" style="top:${b.y || (550 + i * 118)}px"><span class="pill">${b.e ? `<span class="emoji">${b.e}</span> ` : ''}${b.t}</span></div>`).join('')}
  <div id="bsDots" class="abs">${[1,2,3,4,5,6,7].map(i => `<div class="bsDot ${i === C.n ? 'on' : i < C.n ? 'done' : ''}">${i}</div>`).join('')}</div>`);
  const rays = Array.from({length: 7}, (_, i) => { const r = el('div', 'bsRay', $('#bsRays')); return { r, a: 110 + i * 14 }; });
  const cells = makeCells(16, [['#fff3c4','#ffb86b'], ['#ffd1e8','#ff6f91'], ['#d9c8ff','#8a5cff']], 400 + C.n, $('#cells'));
  window.CLIP = {
    duration: C.duration,
    render(t) {
      entryPunch(t); cells.update(t);
      rays.forEach((o, i) => o.r.style.transform = `rotate(${o.a + Math.sin(t * .6 + i) * 3 + t * 2}deg)`);
      $('#bsSun').style.transform = `scale(${1 + Math.sin(t * 1.5) * .03})`;
      css($('#bsStep'), { transform: `translate(-50%,-50%) scale(${pop(t, .1, .4)})`, opacity: t > .1 ? 1 : 0 });
      const h = prog(t, C.hit, .25);
      css($('#bsBadge'), { transform: `scale(${t < C.hit ? 0 : lerp(2.2, 1, ease.back(h))}) rotate(${Math.sin(t * 2) * 3}deg)`, opacity: t > C.hit ? 1 : 0 });
      css($('#bsTile'), { transform: `scale(${pop(t, C.hit + .2, .45)}) rotate(${Math.sin(t * 2.3) * 5}deg) translateY(${Math.sin(t * 3) * 6}px)`, opacity: t > C.hit + .2 ? 1 : 0 });
      $$('#bsTitle .ln').forEach((l, i) => { const a = C.titleAt + i * .18, p = pop(t, a, .45);
        css(l, { transform: `translateX(${lerp(120, 0, ease.out(prog(t, a, .4)))}px) scale(${.7 + .3 * p})`, opacity: t > a ? 1 : 0, transformOrigin: '0 50%' }); });
      C.bullets.forEach((b, i) => { const p = pop(t, b.at, .4);
        css($('#bsB' + i), { transform: `translateX(${lerp(-60, 0, ease.out(prog(t, b.at, .35)))}px) scale(${p})`, opacity: t > b.at ? 1 : 0, transformOrigin: '0 50%' }); });
      $$('.bsDot').forEach((d, i) => d.style.transform = `scale(${pop(t, .2 + i * .05, .3)})`);
      if (C.extra) C.extra(t);
    },
    sfx: [
      [0, 'whoosh', {dur: .45}], [.1, 'pop', {freq: 520}], [C.hit, 'impact', {vol: .6}], [C.hit + .05, 'ding', {freq: 1047 + C.n * 60, dur: 1.0, vol: .25}],
      [C.hit + .2, 'pop', {freq: 760}], [C.titleAt, 'whoosh', {dur: .35, vol: .3}],
      ...C.bullets.map((b, i) => [b.at, 'pop', {freq: 800 + i * 120, vol: .35}]),
      ...(C.extraSfx || []),
    ],
  };
})();
