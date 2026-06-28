# -*- coding: utf-8 -*-
import json
data = json.load(open('season_data2.json', encoding='utf-8'))

NARR = [
 ("cover","新生社様、省エネ・創エネ ダブルプランのご提案です。令和8・令和9の2段階で、太陽光の自家消費、蓄電池、断熱コーティングを導入します。実際の電力データ1年分にもとづくシミュレーションで、現在およそ年500万円の電気代を、最終的に年300万円規模で削減することを目指します。"),
 ("r8","令和8年度です。太陽光を50キロワット増設し、エコメガネとZPDで自家消費を始めます。蓄電池はテスラ4台。屋根には、パネルを貼る前に冷暖断熱トリプルガードコートで防水と遮熱を施します。グラフは春夏秋冬の一日の動きで、黄色が発電、紺色が消費、青が充電、緑が放電です。昼に発電した電気を使い、余りを蓄電池にためて夕方に放電します。既存の太陽光はFIT売電のまま残します。電気代の削減はおよそ年189万円です。"),
 ("r9","令和9年度です。テスラを4台追加して合計8台にし、既存の60キロワットも自家消費へ切り替えて、自家消費の太陽光は合計110キロワットになります。さらに南面の窓ガラスコーティングを施工。発電の黄色が大きくなり、充電も増え、夏の昼の不足をしっかり埋めます。電気代の削減は年337万円規模、ピークカットで最大需要も89キロワットから37キロワットへ下げられます。"),
 ("summary","太陽光パネルが屋根を覆うことで、屋根表面はおよそ25度、屋根裏はおよそ15度下がり、エアコンの消費は10から15パーセント減るという実測研究があります。2階の暑さも和らぎます。補助金は2年でおよそ1700万円。さらに、コーティングなどの余剰を還元し、お客様の実質投資はおよそ1700万円まで圧縮します。年間およそ300万円の削減で、投資回収はおよそ5年台を見込みます。電気代も、暑さ寒さの我慢も、停電対策も、まとめて解決するご提案です。なお記載の数値は試算であり、省エネ診断・正式積算・交付決定で確定します。")
]

import os, base64
# 同じフォルダに cover.mp3 / r8.mp3 / r9.mp3 / summary.mp3 があれば、
# そのNanami音声をHTMLへ埋め込む（全端末で同じ声で再生）。無ければブラウザ音声にフォールバック。
AUDIO_MAP = {}
for _id, _ in NARR:
    _f = _id + '.mp3'
    if os.path.exists(_f) and os.path.getsize(_f) > 0:
        _b = base64.b64encode(open(_f, 'rb').read()).decode('ascii')
        AUDIO_MAP[_id] = 'data:audio/mpeg;base64,' + _b
if AUDIO_MAP:
    print('embedded audio:', list(AUDIO_MAP.keys()))
else:
    print('no mp3 found -> browser voice (Nanami on Windows)')

C={'load':'#0e2a47','pv':'#e0a21e','charge':'#1769aa','discharge':'#15a36b'}
def svg(d, ymax=60):
    W,H=470,212; padL,padR,padT,padB=30,8,10,24
    plotW=W-padL-padR; plotH=H-padT-padB; baseY=padT+plotH; gw=plotW/24.0; bw=gw/4.0
    s=['<svg viewBox="0 0 {} {}" width="100%" xmlns="http://www.w3.org/2000/svg">'.format(W,H)]
    for gv in [0,20,40,60]:
        y=padT+plotH*(1-gv/ymax)
        s.append('<line x1="{}" y1="{:.1f}" x2="{}" y2="{:.1f}" stroke="#e2ebf2"/>'.format(padL,y,W-padR,y))
        s.append('<text x="{}" y="{:.1f}" font-size="9" fill="#8595a4" text-anchor="end">{}</text>'.format(padL-3,y+3,gv))
    series=[('load',C['load']),('pv',C['pv']),('charge',C['charge']),('discharge',C['discharge'])]
    for i in range(24):
        gx=padL+i*gw
        for j,(key,col) in enumerate(series):
            v=d[key][i]
            if v<=0: continue
            h=plotH*(min(v,ymax)/ymax); x=gx+j*bw
            s.append('<rect x="{:.1f}" y="{:.1f}" width="{:.1f}" height="{:.1f}" fill="{}"/>'.format(x,baseY-h,bw*0.92,h,col))
    for hx in [0,6,12,18,23]:
        s.append('<text x="{:.1f}" y="{}" font-size="9" fill="#8595a4" text-anchor="middle">{}時</text>'.format(padL+hx*gw+gw/2,H-8,hx))
    s.append('</svg>'); return ''.join(s)
def charts(yr):
    return ''.join('<div class="chartbox"><h4>{}</h4>{}</div>'.format(s,svg(data[yr][s])) for s in ['春','夏','秋','冬'])
legend=('<span><i style="background:#0e2a47"></i>消費</span><span><i style="background:#e0a21e"></i>発電(太陽光)</span>'
        '<span><i style="background:#1769aa"></i>蓄電(充電)</span><span><i style="background:#15a36b"></i>放電</span>')

HTML='''<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>新生社様 省エネ・創エネ 2段階プラン</title><style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Hiragino Kaku Gothic ProN","Yu Gothic",Meiryo,sans-serif;color:#1b2733;background:#eef2f6;line-height:1.7}
.wrap{max-width:1000px;margin:0 auto;padding:0 16px 80px}
.cover{background:linear-gradient(135deg,#0e2a47,#1769aa);color:#fff;padding:50px 24px;text-align:center;border-radius:0 0 24px 24px}
.cover h1{font-size:28px;margin-bottom:10px}.cover p{font-size:15px;opacity:.92}.cover .cust{margin-top:16px;font-size:16px;font-weight:bold}
.play{margin-top:22px;background:#15a36b;color:#fff;border:none;padding:14px 30px;border-radius:40px;font-size:17px;font-weight:bold;cursor:pointer;box-shadow:0 6px 18px rgba(0,0,0,.25)}
.hl{background:#fff;border-radius:14px;padding:18px;margin:18px 0;box-shadow:0 4px 16px rgba(14,42,71,.08)}
.hl .row{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px}
.hl .b{background:#eaf6ef;border:1px solid #9ed9be;border-radius:12px;padding:12px;text-align:center}
.hl .b .n{font-size:18px;font-weight:bold;color:#0e2a47}.hl .b .l{font-size:11px;color:#5b6b7b}
.yr{background:#fff;border-radius:18px;padding:24px 20px;margin:22px 0;box-shadow:0 4px 16px rgba(14,42,71,.08)}
.yrhead{display:flex;align-items:center;gap:12px;border-left:6px solid #1769aa;padding-left:14px;margin-bottom:16px}
.yrhead .badge{background:#0e2a47;color:#fff;font-size:13px;padding:4px 12px;border-radius:20px;white-space:nowrap}.yrhead h2{font-size:20px}
.items{display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));gap:10px;margin-bottom:14px}
.item{background:#f4f8fb;border:1px solid #d7e3ee;border-radius:12px;padding:12px}
.item .t{font-weight:bold;color:#0e2a47;font-size:13.5px}.item .d{font-size:12px;color:#5b6b7b;margin-top:3px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin:6px 0 16px}
.kpi{background:#eaf6ef;border:1px solid #9ed9be;border-radius:12px;padding:12px;text-align:center}
.kpi .n{font-size:18px;font-weight:bold;color:#0e2a47}.kpi .l{font-size:11px;color:#5b6b7b}
.charts{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:680px){.charts{grid-template-columns:1fr}.cover h1{font-size:23px}}
.chartbox{background:#fafcfe;border:1px solid #e2ebf2;border-radius:12px;padding:10px 8px 6px}.chartbox h4{text-align:center;font-size:14px;color:#0e2a47;margin-bottom:4px}
.legend{display:flex;flex-wrap:wrap;gap:14px;justify-content:center;margin:4px 0 16px;font-size:12px;color:#444}
.legend span{display:inline-flex;align-items:center;gap:5px}.legend i{width:13px;height:13px;border-radius:3px;display:inline-block}
.note{font-size:12px;color:#5b6b7b;background:#fff8e1;border:1px solid #e5c76b;border-radius:10px;padding:10px 12px;margin-top:12px}
.cool{background:#eef6fb;border:1px solid #bcdcee;border-radius:12px;padding:14px;margin:16px 0}
.cool h3{font-size:15px;color:#0e2a47;margin-bottom:6px}.cool p{font-size:12.5px;color:#33414f}
.sum{background:#0e2a47;color:#fff;border-radius:18px;padding:26px 22px;margin-top:22px;text-align:center}
.sum h2{font-size:20px;margin-bottom:14px}.sum .row{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:12px}
.sum .b{background:rgba(255,255,255,.1);border-radius:12px;padding:14px}.sum .b .n{font-size:18px;font-weight:bold}.sum .b .l{font-size:11px;opacity:.85}
.foot{font-size:11px;color:#8595a4;text-align:center;margin-top:20px}.now{outline:3px solid #15a36b;outline-offset:3px;border-radius:18px}
</style></head><body>
<div class="cover" id="s_cover"><h1>省エネ・創エネ ダブルプラン</h1>
<p>令和8・令和9 2段階｜24時間の自家消費シミュレーション</p>
<div class="cust">有限会社新生社ボーン・アゲイン様（八街市）</div>
<button class="play" id="play">&#9654; 自動再生（ナレーション）</button>
<p style="font-size:12px;margin-top:10px;opacity:.8">タップで音声解説が始まります</p></div>
<div class="wrap">
<div class="hl"><div class="row">
<div class="b"><div class="n">約480〜500万円</div><div class="l">現在の年間電気代(推定)</div></div>
<div class="b"><div class="n">約290〜320万円/年</div><div class="l">削減(58〜64%)</div></div>
<div class="b"><div class="n">2年で1,700万円</div><div class="l">千葉県補助金</div></div>
<div class="b"><div class="n">約5.0〜5.7年</div><div class="l">投資回収(NET約1,700万・試算)</div></div>
</div></div>

<div class="yr" id="s_r8"><div class="yrhead"><span class="badge">令和8年度</span><h2>太陽光増設＋自家消費スタート＋屋根防水遮熱</h2></div>
<div class="items">
<div class="item"><div class="t">太陽光増設 50kW（自家消費）</div><div class="d">エコメガネ・ZPD（逆潮流防止）</div></div>
<div class="item"><div class="t">テスラ Powerwall3 ×4台</div><div class="d">蓄電 54kWh</div></div>
<div class="item"><div class="t">冷暖トリプルガードコート 屋根700㎡</div><div class="d">パネル設置前の防水＋遮熱／足場</div></div>
<div class="item"><div class="t">既存太陽光65kW</div><div class="d">FIT売電のまま温存</div></div>
</div>
<div class="kpis"><div class="kpi"><div class="n">約189万円/年</div><div class="l">電気代削減</div></div>
<div class="kpi"><div class="n">89→60kW</div><div class="l">ピークカット</div></div>
<div class="kpi"><div class="n">屋根の暑さ対策</div><div class="l">パネル＋遮熱コート</div></div></div>
<div class="legend">__LEG__</div><div class="charts">__R8__</div>
<div class="note">グラフは平日平均の1日。紺=消費/黄=発電(自家消費50kW)/青=蓄電/緑=放電。昼の発電を使い、余りを蓄電して夕方に放電します。</div></div>

<div class="yr" id="s_r9"><div class="yrhead"><span class="badge">令和9年度</span><h2>既存も自家消費化（計110kW）＋蓄電池8台＋窓断熱</h2></div>
<div class="items">
<div class="item"><div class="t">テスラ Powerwall3 ×4台（計8台）</div><div class="d">蓄電 108kWh</div></div>
<div class="item"><div class="t">既存60kWを自家消費化</div><div class="d">パワコン交換 → 自家消費 計110kW</div></div>
<div class="item"><div class="t">窓ガラスコーティング 90㎡</div><div class="d">南面の日射熱カット</div></div>
<div class="item"><div class="t">高圧接続・各種試験</div><div class="d">連系</div></div>
</div>
<div class="kpis"><div class="kpi"><div class="n">約337万円/年</div><div class="l">電気代削減(実運用290〜320万)</div></div>
<div class="kpi"><div class="n">89→37kW</div><div class="l">ピークカット</div></div>
<div class="kpi"><div class="n">窓＋屋根 遮熱</div><div class="l">空調をさらに圧縮</div></div></div>
<div class="legend">__LEG__</div><div class="charts">__R9__</div>
<div class="note">自家消費が110kWに拡大し、黄(発電)・青(蓄電)が大きく増加。夏の昼の不足を埋め、8台の蓄電池で夕方〜夜・ピークカットに使います。</div></div>

<div class="cool"><h3>☀ 太陽光パネルが屋根を冷やす（2階が涼しくなる根拠）</h3>
<p>パネルが直射日光を遮ることで、実測研究では<b>屋根表面 約25℃低下（70→45℃）／屋根裏 約15℃低下（55→40℃）→ エアコン消費電力 10〜15%削減</b>。トリプルガードコートの遮熱と合わせ、2階の暑さを実際に和らげます。本試算は控えめに空調の約10〜13%で計上。</p></div>

<div class="sum" id="s_summary"><h2>2年トータルのまとめ</h2>
<div class="row">
<div class="b"><div class="n">総工費 4,080万</div><div class="l">令和8 2,580＋令和9 1,500</div></div>
<div class="b"><div class="n">補助 1,700万</div><div class="l">2年・千葉県補助金</div></div>
<div class="b"><div class="n">NET 約1,700万</div><div class="l">余剰還元後・粗利20%(試算)</div></div>
<div class="b"><div class="n">回収 約5.0〜5.7年</div><div class="l">削減約300万/年・IRR約13〜17%</div></div>
</div>
<p style="font-size:13px;margin-top:14px;opacity:.9">電気代も、夏の暑さ・冬の寒さの我慢も、停電対策も、まとめて解決。補助も2年で満額活用します。</p></div>

<div class="foot">株式会社シスコムネット 本社営業部 寺嵜 忠弘｜記載の金額・補助・回収年数・発電量・削減額は実測データに基づく試算です。省エネ診断・正式積算・千葉県の交付決定により確定します。屋根遮熱の出典：エコ発電本舗／SOLSEL／タイナビ。</div>
</div>
<script>
const NARR=__NARR__;const AUDIO=__AUDIO__;let idx=0;let cur=null;let playing=false;
const synth=window.speechSynthesis;let jaVoice=null;
function pickVoice(){const vs=synth.getVoices();jaVoice=vs.find(v=>/nanami/i.test(v.name))||vs.find(v=>/(kyoko|haruka|ayumi|sayaka|o-ren|mizuki)/i.test(v.name))||vs.find(v=>(v.lang||'').toLowerCase().indexOf('ja')===0)||null;}
pickVoice();if('onvoiceschanged' in synth)synth.onvoiceschanged=pickVoice;
function hl(id){document.querySelectorAll('.now').forEach(e=>e.classList.remove('now'));const el=document.getElementById('s_'+id);if(el){el.classList.add('now');el.scrollIntoView({behavior:'smooth',block:'start'});}}
function stopAll(){playing=false;try{synth.cancel();}catch(e){}if(cur){try{cur.pause();}catch(e){}cur=null;}document.querySelectorAll('.now').forEach(e=>e.classList.remove('now'));}
function done(){idx++;setTimeout(nxt,500);}
function nxt(){if(!playing)return;
 if(idx>=NARR.length){playing=false;document.getElementById('play').textContent='\\u25B6 \\u3082\\u3046\\u4e00\\u5ea6';document.querySelectorAll('.now').forEach(e=>e.classList.remove('now'));return;}
 const id=NARR[idx][0];hl(id);
 if(AUDIO[id]){const a=new Audio(AUDIO[id]);cur=a;a.onended=done;a.onerror=done;a.play().catch(()=>{ // 自動再生がブロックされた等の保険でブラウザ音声へ
   const u=new SpeechSynthesisUtterance(NARR[idx][1]);u.lang='ja-JP';if(jaVoice)u.voice=jaVoice;u.onend=done;synth.speak(u);});}
 else{const u=new SpeechSynthesisUtterance(NARR[idx][1]);u.lang='ja-JP';if(jaVoice)u.voice=jaVoice;u.rate=1.0;u.onend=done;synth.speak(u);}}
document.getElementById('play').addEventListener('click',()=>{if(playing){stopAll();document.getElementById('play').textContent='\\u25B6 \\u518d\\u751f';return;}stopAll();playing=true;idx=0;document.getElementById('play').textContent='\\u25A0 \\u505c\\u6b62';nxt();});
</script></body></html>'''
html=HTML.replace('__NARR__',json.dumps(NARR,ensure_ascii=False)).replace('__AUDIO__',json.dumps(AUDIO_MAP,ensure_ascii=False)).replace('__R8__',charts('r8')).replace('__R9__',charts('r9')).replace('__LEG__',legend)
open('新生社様_2段階プラン_24h自家消費シミュレーション.html','w',encoding='utf-8').write(html)
print('HTML written',len(html))
