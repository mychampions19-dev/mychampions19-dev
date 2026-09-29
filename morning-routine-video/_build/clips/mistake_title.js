// Reusable "MISTAKE #N" title card. A clip sets window.MT = {n, icon, line1, line2, tile:[c1,c2], hit, subAt, duration}
// then loads this file. hit = when the number slams (sync to "mistake number N"), subAt = when the subtitle pops.
(function () {
  const C = window.MT;
  document.getElementById('stage').insertAdjacentHTML('beforeend', `
  <style>
    .tape { position:absolute; left:-300px; width:2520px; height:90px; transform-origin:50% 50%;
      background: repeating-linear-gradient(135deg, #ffd166 0 60px, #1b0f45 60px 120px);
      box-shadow: 0 10px 30px rgba(0,0,0,.5); }
    #mtWord { left:640px; top:250px; font-size:120px; }
    #mtBadge { left:640px; top:490px; width:330px; height:330px; margin:-165px 0 0 -165px; --c1:#ff7b8f; --c2:#c0213a; }
    #mtNum { position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); font-size:210px; font-weight:700; color:#fff;
      text-shadow: 5px 0px 0 #5a0a1e, -5px 0px 0 #5a0a1e, 0px 5px 0 #5a0a1e, 0px -5px 0 #5a0a1e, 4px 4px 0 #5a0a1e, -4px 4px 0 #5a0a1e, 4px -4px 0 #5a0a1e, -4px -4px 0 #5a0a1e, 0 10px 0 #5a0a1e, 0 16px 26px rgba(0,0,0,.45); white-space:nowrap; }
    #mtTile { left:1300px; top:430px; width:420px; height:420px; margin:-210px 0 0 -210px; border-radius:90px;
      box-shadow: inset 0 8px 0 rgba(255,255,255,.45), inset 0 -16px 0 rgba(0,0,0,.2), 0 30px 60px rgba(0,0,0,.5); }
    #mtIcon { position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); font-size:240px; }
    #mtSub { left:960px; top:790px; text-align:center; }
    #mtSub .pill { font-size:64px; background: linear-gradient(135deg, #ff3b5c, #9b5cff); }
    #mtDots { left:960px; top:900px; transform:translateX(-50%); display:flex; gap:22px; }
    .mtDot { width:54px; height:54px; border-radius:50%; background:rgba(255,255,255,.15); font:700 30px 'Fredoka';
      display:flex; align-items:center; justify-content:center; color:rgba(255,255,255,.5); }
    .mtDot.on { background:#ff3b5c; color:#fff; box-shadow:0 0 24px #ff3b5c; }
    .mtDot.done { background:rgba(46,230,168,.35); color:#fff; }
  </style>
  <div class="tape" id="tape1" style="top:20px"></div><div class="tape" id="tape2" style="top:1010px"></div>
  <div id="mtWord" class="abs h3d warn">MISTAKE</div>
  <div id="mtBadge" class="abs glossy"><div id="mtNum">#${C.n}</div></div>
  <div id="mtTile" class="abs" style="background:linear-gradient(160deg, ${C.tile[0]}, ${C.tile[1]})"><div id="mtIcon" class="emoji">${C.icon}</div></div>
  <div id="mtSub" class="abs"><span class="pill">${C.line1}</span></div>
  <div id="mtDots" class="abs">${[1,2,3,4,5,6,7].map(i => `<div class="mtDot ${i === C.n ? 'on' : i < C.n ? 'done' : ''}">${i}</div>`).join('')}</div>`);

  const cells = makeCells(22, [['#ff6b6b','#b3122e'], ['#9b5cff','#3d1c8f'], ['#ffb13b','#c2551f']], 40 + C.n, $('#cells'));
  window.CLIP = {
    duration: C.duration,
    render(t) {
      entryPunch(t); cells.update(t);
      const tp = ease.out(prog(t, 0, .45));
      $('#tape1').style.transform = `translateX(${lerp(-2600, 0, tp) + t * 40}px) rotate(-3deg)`;
      $('#tape2').style.transform = `translateX(${lerp(2600, 0, tp) - t * 40}px) rotate(-3deg)`;
      const wp = pop(t, .2, .45);
      css($('#mtWord'), { transform: `translate(-50%,-50%) scale(${wp})`, opacity: t > .2 ? 1 : 0 });
      const s = prog(t, C.hit, .25);
      css($('#mtBadge'), { transform: `scale(${t < C.hit ? 0 : lerp(2.6, 1, ease.back(s))}) rotate(${lerp(-25, 0, ease.out(s)) + Math.sin(t*2)*2}deg)`,
        opacity: t > C.hit ? 1 : 0 });
      const ip = pop(t, C.hit + .25, .5);
      css($('#mtTile'), { transform: `scale(${ip}) rotate(${Math.sin(t * 2.2) * 4}deg) translateY(${Math.sin(t*3)*8}px)`, opacity: t > C.hit + .25 ? 1 : 0 });
      const buzz = C.shakeIcon && t > C.hit + .6 ? Math.sin(t * 70) * 5 : 0;
      $('#mtIcon').style.transform = `translate(calc(-50% + ${buzz}px), -50%)`;
      const sp = pop(t, C.subAt, .45);
      css($('#mtSub'), { transform: `translate(-50%,-50%) scale(${sp})`, opacity: t > C.subAt ? 1 : 0 });
      $$('.mtDot').forEach((d, i) => { const p = pop(t, .35 + i * .06, .35); d.style.transform = `scale(${p})`; });
      const sk = t > C.hit && t < C.hit + .3 ? Math.sin(t * 120) * 10 * (1 - prog(t, C.hit, .3)) : 0;
      $('#stage').style.transform += ` translate(${sk}px,0)`;
    },
    sfx: [
      [0, 'whoosh', {dur: .5}], [.2, 'pop', {freq: 520}],
      ...[0,1,2,3,4,5,6].map(i => [.35 + i * .06, 'tick', {vol: .2}]),
      [C.hit, 'impact', {vol: .85}], [C.hit + .25, 'pop', {freq: 760}], [C.subAt, 'pop', {freq: 600, vol: .35}],
      ...(C.extraSfx || []),
    ],
  };
})();
