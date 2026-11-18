#!/usr/bin/env python3
"""Generate the Night Fleet scene (v3): a cinematic dark space-opera battle.

An armored dark lord in a crested helmet, red visor glowing in time with his
breathing, stands on a red-lit deck with a humming red blade raised toward the
battle. Behind him a dying red world; overhead a black dreadnought with escorts
pours red fire on fleeing interceptors while fleet fighters hunt them down.
All original art: no franchise ships, characters or logos.

Usage: gen_fleet.py <out_dir> [scene.ts path]
"""
import math
import random
import sys

random.seed(11)
W, H = 1600, 1000


def f(x):
    return f"{x:.1f}".rstrip('0').rstrip('.')


# ---------------------------------------------------------------- stars
def star_layer(n, rmin, rmax, omin, omax, twinkle=False, ymax=0.93):
    stars = []
    for _ in range(n):
        x, y = random.uniform(0, W), random.uniform(0, H * ymax)
        stars.append((x, y, random.uniform(rmin, rmax), random.uniform(omin, omax),
                      random.choice(['#ffffff', '#ffffff', '#ffe4de', '#ffd2c8', '#dfe6ff'])))
    out = []
    for dx in (0, W):
        for i, (x, y, r, o, tint) in enumerate(stars):
            extra = ''
            if twinkle and i % 3 == 0:
                extra = f' class="tw" style="animation-delay:-{f(random.uniform(0, 6))}s"'
            out.append(f'<circle cx="{f(x + dx)}" cy="{f(y)}" r="{f(r)}" fill="{tint}" opacity="{f(o)}"{extra}/>')
    return ''.join(out)


far = star_layer(150, 0.45, 0.85, 0.25, 0.6)
mid = star_layer(55, 0.9, 1.35, 0.5, 0.85, twinkle=True)
near = star_layer(12, 1.5, 2.0, 0.75, 1.0, twinkle=True)

# a faint galactic band across the sky
GALAXY = ''.join(
    f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(random.uniform(.3,.7))}" fill="#ffd8d0" opacity="{f(random.uniform(.15,.45))}"/>'
    for x, y in ((t + random.gauss(0, 18), 560 - t * 0.42 + random.gauss(0, 34))
                 for t in (random.uniform(-100, 1700) for _ in range(260))))


# ---------------------------------------------------------------- fighters
def fighter(trail=True):
    t = ('<rect x="-120" y="-2.2" width="96" height="4.4" rx="2.2" fill="url(#trailR)"/>' if trail else '')
    return (
        '<g>' + t +
        '<polygon points="5,-4 -12,-29 -24,-29 -11,-4" fill="url(#hullG)" stroke="#3a3f49" stroke-width=".8" stroke-opacity=".45"/>'
        '<polygon points="5,4 -12,29 -24,29 -11,4" fill="url(#hullG)" stroke="#3a3f49" stroke-width=".8" stroke-opacity=".45"/>'
        '<polygon points="-12,-29 -24,-29 -26,-33 -10,-33" fill="#d0283a"/>'
        '<polygon points="-12,29 -24,29 -26,33 -10,33" fill="#d0283a"/>'
        '<polygon points="35,0 15,-6.5 -16,-5.5 -22,0 -16,5.5 15,6.5" fill="#1b1e25"/>'
        '<polygon points="35,0 15,-6.5 -16,-5.5 -22,0" fill="#262a33"/>'
        '<ellipse cx="12" cy="0" rx="7" ry="3" fill="#d42a3a" opacity=".85"/>'
        '<circle class="eng" cx="-24" cy="0" r="7.5" fill="url(#engR)"/>'
        '</g>')


FIGHTER = fighter()


def bolts(delay, color='#ff2d3d'):
    """Twin wing cannons: two streaks fly ahead of the nose and fade."""
    one = (f'<line x1="24" y1="{{y}}" x2="62" y2="{{y}}" stroke="{color}" stroke-width="7" stroke-opacity=".25" stroke-linecap="round"/>'
           f'<line x1="24" y1="{{y}}" x2="62" y2="{{y}}" stroke="#ffeaea" stroke-width="1.9" stroke-linecap="round"/>')
    return f'<g class="bolt" style="animation-delay:{delay}s">{one.format(y=-10)}{one.format(y=10)}</g>'


# the opposing interceptor: a single grey-blue delta with a cyan engine
INTERCEPTOR = (
    '<g>'
    '<rect x="-110" y="-2" width="88" height="4" rx="2" fill="url(#trailB)"/>'
    '<polygon points="30,0 -18,-16 -12,0 -18,16" fill="#5f6f79"/>'
    '<polygon points="30,0 -18,-16 -12,0" fill="#6d7e88"/>'
    '<ellipse cx="8" cy="0" rx="5" ry="2" fill="#0d2230"/>'
    '<circle class="eng" cx="-14" cy="0" r="5.5" fill="url(#engB)"/>'
    '</g>'
)


# ---------------------------------------------------------------- dreadnought
def hull_top(x):
    pts = [(0, -14), (150, -26), (440, -34), (580, -40), (700, -36)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return -36


def capital(with_guns=True, detail=True):
    parts = []
    if with_guns:
        for gx, d in [(260, 0), (390, -1.3), (520, -2.4), (330, -3.1), (450, -3.7)]:
            parts.append(
                f'<g transform="translate({gx},40) rotate(150)"><g class="tbolt" style="animation-delay:{d}s">'
                '<line x1="0" y1="0" x2="52" y2="0" stroke="#ff2233" stroke-width="8" stroke-opacity=".28" stroke-linecap="round"/>'
                '<line x1="0" y1="0" x2="52" y2="0" stroke="#ffe4e4" stroke-width="2.3" stroke-linecap="round"/>'
                '</g></g>')
    parts.append('<ellipse cx="780" cy="0" rx="130" ry="30" fill="url(#plume)" class="cengs"/>')
    parts.append(
        # forked bow, long hull, low dorsal spine with one raked sail, ventral keel
        '<polygon points="0,-14 150,-26 440,-34 580,-40 700,-36 700,36 580,40 440,34 150,26 0,14 110,5 110,-5" fill="url(#capG)"/>'
        '<polygon points="0,-14 150,-26 440,-34 440,-28 150,-21 12,-10" fill="#3a404b"/>'
        '<polygon points="160,-14 450,-34 450,-15 160,-5" fill="#13161c"/>'
        '<polygon points="110,-5 110,5 0,14 4,10 100,3 100,-3 4,-10 0,-14" fill="#07080b"/>'
        '<polygon points="300,-31 380,-56 600,-56 650,-38" fill="#1a1e25"/>'
        '<polygon points="300,-31 380,-56 600,-56 602,-52 384,-52" fill="#2c313b"/>'
        '<polygon points="470,-56 530,-92 562,-92 600,-56" fill="#20242c"/>'
        '<rect x="528" y="-84" width="30" height="2.5" fill="#ff3b3b" opacity=".9"/>'
        '<circle cx="546" cy="-94" r="2.4" fill="#ff2d3d" class="blink"/>'
        '<polygon points="360,34 470,84 500,84 520,38" fill="#0a0c10"/>'
        '<polygon points="360,34 470,84 474,84 366,34" fill="#2c313b"/>'
        '<line x1="470" y1="84" x2="500" y2="84" stroke="#ff2d3d" stroke-width="1.4" stroke-opacity=".7"/>'
        '<line x1="150" y1="0" x2="700" y2="0" stroke="#ff2d3d" stroke-width="1" stroke-opacity=".45"/>'
        '<line x1="320" y1="-29" x2="320" y2="29" stroke="#0d0f14" stroke-width="2.5"/>'
        '<line x1="490" y1="-36" x2="490" y2="36" stroke="#0d0f14" stroke-width="2.5"/>'
    )
    if detail:
        g = []
        for _ in range(70):
            x = random.uniform(150, 660)
            top = hull_top(x)
            y = random.uniform(top + 3, -6)
            w, h = random.uniform(4, 16), random.uniform(1.5, 4)
            g.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{random.choice(["#272b34", "#1a1d24", "#323844"])}"/>')
        parts.append(''.join(g))
        lights = []
        for y, x0, x1 in [(-12, 170, 640), (-3, 130, 670), (8, 140, 660), (19, 190, 620)]:
            x = x0
            while x < x1:
                if random.random() < 0.5:
                    red = random.random() < 0.2
                    cls = f' class="blink" style="animation-delay:-{f(random.uniform(0, 9))}s"' if random.random() < 0.12 else ''
                    lights.append(f'<rect x="{f(x)}" y="{y}" width="2.4" height="1.3" fill="{"#ff3b3b" if red else "#ffcfb0"}" opacity=".8"{cls}/>')
                x += random.uniform(5, 11)
        parts.append(''.join(lights))
    parts.append(
        '<g class="cengs">'
        '<circle cx="706" cy="-19" r="19" fill="url(#engR)"/>'
        '<circle cx="706" cy="0" r="24" fill="url(#engR)"/>'
        '<circle cx="706" cy="19" r="19" fill="url(#engR)"/>'
        '</g>')
    return '<g>' + ''.join(parts) + '</g>'


def escort():
    """A small frigate flying with the dreadnought."""
    return ('<g>'
            '<polygon points="0,-5 60,-9 150,-11 170,-9 170,9 150,11 60,9 0,5 26,0" fill="url(#capG)"/>'
            '<polygon points="110,-11 126,-19 150,-19 158,-10" fill="#1d2128"/>'
            '<line x1="60" y1="0" x2="170" y2="0" stroke="#ff2d3d" stroke-width=".8" stroke-opacity=".6"/>'
            '<circle class="cengs" cx="174" cy="0" r="9" fill="url(#engR)"/>'
            '</g>')


CAP = capital()
CAP_FAR = capital(with_guns=False, detail=False)
ESC = escort()


def flash(x, y, delay, size=1.0):
    return (f'<g transform="translate({x},{y}) scale({size})"><g class="boom" style="animation-delay:{delay}s">'
            '<circle r="16" fill="url(#boomG)"/><circle r="10" fill="none" stroke="#ff9a6b" stroke-width="1.4"/>'
            '</g></g>')


def jump(x, y, delay):
    lines = ''.join(
        f'<line x1="0" y1="{dy}" x2="{-ln}" y2="{dy}" stroke="#ffe6e6" stroke-width="1.4" stroke-opacity="{o}" stroke-linecap="round"/>'
        for dy, ln, o in [(-6, 240, .9), (-2, 330, 1), (2, 280, .9), (6, 200, .7), (-10, 150, .5), (10, 170, .5)])
    return (f'<g transform="translate({x},{y}) rotate(-8)"><g class="jump" style="animation-delay:{delay}s">'
            f'{lines}<circle r="5" fill="#ffffff"/></g></g>')



# ---------------------------------------------------------------- dying world
def planet():
    bands = ''.join(
        f'<rect x="-300" y="{y}" width="600" height="{h}" fill="{c}" opacity="{o}"/>'
        for y, h, c, o in [(-130, 22, '#000000', .12), (0, 26, '#000000', .12), (130, 24, '#000000', .12)])
    cracks = ('<path d="M-160,-46 L-128,-30 L-110,-38 M-128,-30 L-120,-12 M-30,10 L0,0 L18,-14 M0,0 L10,16 '
              'M60,60 L92,48 L104,58 M92,48 L96,32 M-90,120 L-62,110" '
              'fill="none" stroke="#ff4a2a" stroke-width="1.2" stroke-opacity=".6" class="lava"/>')
    return (
        '<g class="planetPos"><g transform="translate(1240,900) rotate(-14) scale(1.38)">'
        '<circle r="345" fill="url(#atmoGlow)" class="glowpulse"/>'
        '<circle r="290" fill="url(#planetG)"/>'
        f'<g clip-path="url(#planetClip)">{bands}</g>'
        '<circle r="290" fill="url(#shadeG)"/>'
        '</g></g>'
    )


# ---------------------------------------------------------------- the dark lord
# Local frame: feet at (0,0), crest tip near y=-622, three-quarter view facing left.
RIM = '#ff3a2a'
KEY = '#ff2030'
LORD = (
    '<ellipse cx="-20" cy="0" rx="230" ry="24" fill="url(#spill)"/>'
    # cape: three lobes hung from the shoulders, each swaying on its own
    '<g class="lobeB">'
    '<path d="M0,-494 C90,-470 190,-300 272,-24 C240,-34 214,-10 196,-26 L186,-44 L172,-20 C150,-28 128,-22 110,-30 C96,-200 60,-380 0,-494 Z" fill="#050507"/>'
    '<path d="M272,-24 C255,-42 238,-48 224,-30 C240,-27 256,-22 272,-24 Z" fill="#2a0608"/>'
    '<path d="M30,-480 C84,-330 132,-170 166,-30 L150,-28 C118,-170 72,-330 30,-480 Z" fill="#000" opacity=".8"/>'
    f'<path d="M0,-494 C90,-470 160,-380 214,-220 C160,-372 84,-462 0,-494 Z" fill="{RIM}" opacity=".4"/>'
    '</g>'
    '<g class="lobeM">'
    '<path d="M-10,-496 C60,-460 140,-300 190,-6 C160,-14 132,-2 112,-12 L100,-28 L90,-10 C76,-180 40,-360 -10,-496 Z" fill="#09090d"/>'
    '<path d="M20,-470 C70,-330 104,-170 124,-14 L112,-12 C94,-170 60,-330 20,-470 Z" fill="#000" opacity=".7"/>'
    '</g>'
    '<g class="lobeN">'
    '<path d="M-10,-496 C10,-380 24,-200 20,-6 C44,-2 70,-6 90,0 C70,-180 40,-360 -10,-496 Z" fill="#060608"/>'
    '</g>'
    # far arm, fist clenched at the hip
    '<polygon points="62,-470 92,-452 98,-372 84,-296 60,-300 66,-380" fill="#0a0a0d"/>'
    '<polygon points="58,-300 88,-296 86,-272 60,-276" fill="#111216"/>'
    f'<polygon points="92,-452 98,-372 84,-296 88,-298 101,-372 95,-450" fill="{RIM}" opacity=".3"/>'
    # far leg, planted
    '<polygon points="-4,-312 36,-312 56,-170 14,-166" fill="#07070a"/>'
    '<polygon points="14,-166 56,-170 70,-20 34,-20" fill="#07070a"/>'
    '<polygon points="26,-20 74,-20 80,0 14,0" fill="#0a0a0d"/>'
    # near leg, stepping forward
    '<polygon points="-40,-312 2,-312 -22,-170 -74,-178" fill="#0e0f13"/>'
    '<polygon points="-80,-190 -18,-184 -24,-158 -76,-162" fill="#1b1c23"/>'
    '<polygon points="-74,-162 -24,-158 -52,-22 -92,-22" fill="#0e0f13"/>'
    '<polygon points="-104,-22 -48,-22 -44,0 -134,0" fill="#121318"/>'
    f'<polygon points="-40,-312 -30,-312 -62,-177 -74,-178" fill="{KEY}" opacity=".18"/>'
    f'<polygon points="-74,-162 -66,-161 -86,-22 -92,-22" fill="{KEY}" opacity=".15"/>'
    # torso, pauldrons and helm rise and fall with each breath
    '<g class="breath">'
    '<polygon points="-44,-314 -6,-314 -14,-236 -52,-250" fill="#121318"/>'
    '<polygon points="0,-314 36,-314 44,-248 8,-236" fill="#0c0c10"/>'
    '<rect x="-36" y="-330" width="70" height="16" fill="#101115"/>'
    '<polygon points="-3,-330 5,-322 -3,-314 -11,-322" fill="#1b1c23"/>'
    '<polygon points="-78,-492 70,-496 44,-380 30,-330 -34,-330 -58,-384" fill="url(#armorG)"/>'
    '<path d="M-78,-492 L-14,-492 C-26,-430 -22,-370 -10,-330 L-34,-330 L-58,-384 Z" fill="#1b1c23"/>'
    '<path d="M-14,-492 C-26,-430 -22,-370 -10,-330" fill="none" stroke="#050507" stroke-width="2"/>'
    '<path d="M-52,-470 L-12,-442 L40,-474 M-46,-444 L-10,-416 L36,-446" fill="none" stroke="#050507" stroke-width="2.5"/>'
    '<rect class="core" x="-15" y="-436" width="3" height="30" fill="#ff2a2a"/>'
    # far pauldron
    '<polygon points="30,-510 92,-504 104,-452 76,-440 46,-476" fill="#121318"/>'
    f'<polygon points="30,-510 92,-504 104,-452 100,-454 89,-500 30,-506" fill="{RIM}" opacity=".7"/>'
    # gorget
    # helm, nodding forward a touch on each breath
    # trapezius slopes and a standing collar behind the helm
    '<polygon points="-30,-516 -88,-512 -60,-500 -26,-498" fill="#0c0c10"/>'
    '<polygon points="28,-518 92,-504 60,-498 24,-498" fill="#0c0c10"/>'
    '<polygon points="-2,-498 44,-504 60,-566 40,-548 22,-520" fill="#08080b"/>'
    f'<polygon points="44,-504 60,-566 56,-560 41,-506" fill="{RIM}" opacity=".6"/>'
    '<path d="M-34,-516 C-24,-534 22,-536 32,-518 L24,-496 L-26,-496 Z" fill="#060608"/>'
    '<g class="nod"><g transform="translate(-4,-516) scale(1.16) translate(4,516)">'
    '<polygon points="-8,-590 40,-604 62,-596 22,-578" fill="#0d0e12"/>'
    f'<polygon points="40,-604 62,-596 22,-578 20,-582 57,-597" fill="{RIM}" opacity=".8"/>'
    '<polygon points="-36,-530 -40,-562 -24,-586 6,-590 26,-572 28,-538 14,-522 -22,-516" fill="url(#helmG)"/>'
    '<polygon points="-36,-530 -40,-562 -24,-586 -10,-558 -22,-516" fill="#1b1c23"/>'
    '<path d="M-24,-586 L-10,-558 L-22,-516 M-10,-558 L26,-572" fill="none" stroke="#050507" stroke-width="1.5"/>'
    f'<polygon points="6,-590 26,-572 28,-538 25,-540 23,-570 4,-587" fill="{RIM}" opacity=".8"/>'
    f'<polygon points="-36,-530 -22,-516 -28,-540" fill="{KEY}" opacity=".2"/>'
    '<ellipse class="visorglow" cx="-24" cy="-556" rx="30" ry="10" fill="url(#visorG)"/>'
    '<polygon class="visor" points="-42,-552 -8,-561 -7,-557 -41,-549" fill="#ff3030"/>'
    '</g></g>'
    # near pauldron, over the chest
    '<path d="M-112,-470 L-88,-512 L-30,-514 L-18,-484 L-60,-452 Z" fill="#16171d"/>'
    '<path d="M-100,-478 L-78,-506 L-34,-506" fill="none" stroke="#22232a" stroke-width="1.5"/>'
    '<polygon points="-118,-452 -66,-436 -70,-420 -114,-436" fill="#101116"/>'
    f'<polygon points="-112,-470 -60,-452 -64,-458 -108,-474" fill="{KEY}" opacity=".2"/>'
    '</g>'
    # sword arm: upper arm, forearm, flared gauntlet cuff, fist
    '<polygon points="-112,-486 -72,-468 -92,-370 -130,-378" fill="#0e0f13"/>'
    '<polygon points="-130,-378 -92,-370 -110,-286 -140,-292" fill="#0e0f13"/>'
    '<polygon points="-136,-344 -84,-330 -108,-282 -146,-292" fill="#1b1c23"/>'
    '<polygon points="-142,-292 -114,-284 -118,-262 -148,-270" fill="#141519"/>'
    f'<polygon points="-142,-292 -136,-290 -142,-268 -148,-270" fill="{KEY}" opacity=".22"/>'
    # the blade in a low guard, humming, lighting the deck
    '<ellipse class="bladeglow" cx="-228" cy="-30" rx="110" ry="6" fill="#ff2a2a" opacity=".35"/>'
    '<ellipse class="bladeglow" cx="-228" cy="-30" rx="44" ry="1" fill="#ffd6d6" opacity=".3"/>'
    '<g transform="translate(-132,-268) rotate(118)">'
    '<ellipse class="bladeglow" cx="132" cy="0" rx="150" ry="24" fill="url(#bladeHalo)"/>'
    '<g class="blade">'
    '<line x1="14" y1="0" x2="232" y2="0" stroke="#ff1a2a" stroke-width="26" stroke-opacity=".1"/>'
    '<line x1="14" y1="0" x2="232" y2="0" stroke="#ff1a2a" stroke-width="13" stroke-opacity=".3"/>'
    '<polygon points="14,-8.8 218,-3.5 232,0 218,3.5 14,8.8" fill="#ff3a44"/>'
    '<polygon points="14,-4 218,-1.6 232,0 218,1.6 14,4" fill="#fff2f2"/>'
    '</g>'
    '<rect x="-44" y="-4" width="56" height="8" fill="#15161b"/>'
    '<polygon points="-44,-4 -56,0 -44,4" fill="#2a2d33"/>'
    '</g>'
)

import sys as _s, os as _o
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
from lord import LORD, LORD_DEFS, LORD_CSS  # noqa: E402  the v6 dark lord replaces the old figure

FOG_BACK = ''.join(
    f'<ellipse class="fog" style="animation-delay:-{d}s" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#fogG)"/>'
    for cx, cy, rx, ry, d in [(90, -10, 160, 22, 6), (-190, -6, 140, 18, 11)])
FOG_FRONT = '<ellipse class="fog" cx="-50" cy="-4" rx="180" ry="22" fill="url(#fogG)" opacity=".5"/>'
EMBERS = ''.join(
    f'<circle class="ember" style="animation-duration:{f(random.uniform(9, 14))}s;animation-delay:-{f(random.uniform(0, 14))}s" '
    f'cx="{f(random.uniform(-220, 220))}" cy="{f(random.uniform(-30, 0))}" r="{f(random.uniform(.8, 1.6))}" fill="#ff6a4a"/>'
    for _ in range(12))

WARLORD = (f'<g class="lordPos"><g transform="translate(1175,1000) scale(.93)">'
           f'{FOG_BACK}{LORD}{FOG_FRONT}{EMBERS}</g></g>')


def deck():
    vp = (700, 900)
    seams = []
    for x0 in range(880, 1720, 110):
        t = (1000 - 944) / (1000 - vp[1])
        seams.append(f'<line x1="{x0}" y1="1000" x2="{f(x0 + (vp[0] - x0) * t)}" y2="944"/>')
    return (
        '<g class="lordPos">'
        '<clipPath id="deckClip"><polygon points="820,1000 905,944 1600,944 1600,1000"/></clipPath>'
        '<polygon points="820,1000 905,944 1600,944 1600,1000" fill="url(#deckG)"/>'
        f'<g stroke="#17181d" stroke-width="1.2" clip-path="url(#deckClip)">{"".join(seams)}</g>'
        '<line x1="905" y1="944" x2="1600" y2="944" stroke="#ff2d3d" stroke-width="2" stroke-opacity=".45"/>'
        '</g>')


DECK = deck()

STYLE = """
.drift-far{animation:scroll 280s linear infinite}
.drift-mid{animation:scroll 160s linear infinite}
.drift-near{animation:scroll 95s linear infinite}
@keyframes scroll{to{transform:translateX(-1600px)}}
.tw{animation:tw 4.5s ease-in-out infinite}
@keyframes tw{50%{opacity:.25}}
.neb{animation:breathe 22s ease-in-out infinite}
.neb2{animation:breathe 30s ease-in-out infinite reverse}
@keyframes breathe{50%{opacity:.6}}
.glowpulse{animation:glow 5s ease-in-out infinite}
@keyframes glow{50%{opacity:.7}}
.eng{animation:flick .18s steps(2) infinite}
@keyframes flick{50%{opacity:.7}}
.cengs{animation:pulse 3.2s ease-in-out infinite}
@keyframes pulse{50%{opacity:.7}}
.blink{animation:blink 2.6s steps(1) infinite}
@keyframes blink{50%{opacity:.15}}
.lava{animation:glow 3.4s ease-in-out infinite}
.capmove{animation:capmove 180s linear infinite;animation-delay:-66s}
@keyframes capmove{from{transform:translateX(1780px)}to{transform:translateX(-1000px)}}
.capfar{animation:capmove 320s linear infinite;animation-delay:-140s}
.sqA{animation:sqA 22s linear infinite;animation-delay:-5.5s}
@keyframes sqA{0%{transform:translate(-320px,270px)}40%{transform:translate(1920px,505px)}100%{transform:translate(1920px,505px)}}
.sqD{animation:sqD 27s linear infinite;animation-delay:-19s}
@keyframes sqD{0%{transform:translate(-320px,120px)}36%{transform:translate(1920px,230px)}100%{transform:translate(1920px,230px)}}
.sqB{animation:sqB 29s linear infinite;animation-delay:-6.5s}
.sqC{animation:sqB 29s linear infinite;animation-delay:-5.3s}
@keyframes sqB{0%{transform:translate(1920px,640px)}40%{transform:translate(-320px,520px)}100%{transform:translate(-320px,520px)}}
.doomed{animation:doomed 29s linear infinite;animation-delay:-6.5s}
@keyframes doomed{0%,23.9%{opacity:1}24%,100%{opacity:0}}
.kill{animation:kill 29s ease-out infinite;animation-delay:-6.5s;opacity:0;transform-box:fill-box;transform-origin:center}
@keyframes kill{0%,23.9%{opacity:0;transform:scale(.3)}24%{opacity:1;transform:scale(.6)}29%{opacity:0;transform:scale(2.2)}100%{opacity:0;transform:scale(2.2)}}
.bolt{animation:bolt 1.4s linear infinite;opacity:0}
@keyframes bolt{0%{transform:translateX(0);opacity:1}40%{transform:translateX(440px);opacity:0}100%{transform:translateX(440px);opacity:0}}
.tbolt{animation:tbolt 4.2s linear infinite;opacity:0}
@keyframes tbolt{0%{transform:translateX(0);opacity:1}30%{transform:translateX(640px);opacity:0}100%{transform:translateX(640px);opacity:0}}
.boom{animation:boom 11s ease-out infinite;opacity:0;transform-box:fill-box;transform-origin:center}
@keyframes boom{0%{opacity:0;transform:scale(.2)}2%{opacity:1;transform:scale(.6)}9%{opacity:0;transform:scale(1.7)}100%{opacity:0;transform:scale(1.7)}}
.jump{animation:jump 17s ease-in infinite;opacity:0;transform-box:fill-box;transform-origin:right center}
@keyframes jump{0%{opacity:0;transform:scaleX(.02)}1%{opacity:1;transform:scaleX(.02)}4%{opacity:1;transform:scaleX(1)}7%{opacity:0;transform:scaleX(1.4) translateX(-120px)}100%{opacity:0}}
.blade{animation:hum .16s steps(2) infinite}
@keyframes hum{50%{opacity:.93}}
.bladeglow{animation:surge 2.7s ease-in-out infinite}
@keyframes surge{50%{opacity:.6}}
.lobeB{animation:lobeB 7s ease-in-out infinite;transform-box:fill-box;transform-origin:0 0}
@keyframes lobeB{50%{transform:skewX(-4deg) scaleX(1.04)}}
.lobeM{animation:lobeM 5.3s ease-in-out infinite;animation-delay:-2s;transform-box:fill-box;transform-origin:0 0}
@keyframes lobeM{50%{transform:skewX(-2.5deg)}}
.lobeN{animation:lobeN 9s ease-in-out infinite;animation-delay:-4s;transform-box:fill-box;transform-origin:30% 0}
@keyframes lobeN{50%{transform:skewX(1.5deg)}}
.nod{animation:nod 4.8s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 100%}
@keyframes nod{0%,100%{transform:rotate(0)}45%{transform:rotate(-1.5deg)}}
.ember{animation-name:ember;animation-timing-function:linear;animation-iteration-count:infinite;opacity:0}
@keyframes ember{0%{transform:translateY(0);opacity:0}15%{opacity:.8}100%{transform:translateY(-120px);opacity:0}}
.breath{animation:breath 4.8s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 100%}
@keyframes breath{0%,100%{transform:scale(1,1)}45%{transform:scale(1.012,1.008) translateY(-1.5px)}}
.visor{animation:visor 4.8s ease-in-out infinite}
.visorglow{animation:visor 4.8s ease-in-out infinite}
@keyframes visor{0%,100%{opacity:.7}45%{opacity:1}}
.core{animation:core 4.8s ease-in-out infinite}
@keyframes core{0%,100%{opacity:.45}45%{opacity:1}}
.fog{animation:fog 16s ease-in-out infinite alternate}
@keyframes fog{from{transform:translateX(-26px);opacity:.55}to{transform:translateX(30px);opacity:.9}}
@media (max-aspect-ratio:3/4){
  .planetPos{transform:translate(-470px,0)}
  .lordPos{transform:translate(-50px,250px) scale(.75)}
  .capPos{transform:translate(0,40px) scale(.7)}
}
@media (min-aspect-ratio:3/4) and (max-aspect-ratio:5/4){.lordPos{transform:translate(40px,0)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}.bolt,.tbolt,.boom,.jump,.kill,.ember{opacity:0}}
"""

DEFS = """
<radialGradient id="space" cx="72%" cy="62%" r="90%"><stop offset="0" stop-color="#2c0508"/><stop offset=".45" stop-color="#0c0406"/><stop offset="1" stop-color="#020203"/></radialGradient>
<radialGradient id="nebR"><stop offset="0" stop-color="#b80f1e" stop-opacity=".55"/><stop offset=".5" stop-color="#5a0812" stop-opacity=".25"/><stop offset="1" stop-color="#2a0408" stop-opacity="0"/></radialGradient>
<radialGradient id="nebD"><stop offset="0" stop-color="#3a0610" stop-opacity=".6"/><stop offset="1" stop-color="#120206" stop-opacity="0"/></radialGradient>
<radialGradient id="vig" cx="50%" cy="48%" r="75%"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".7"/></radialGradient>
<linearGradient id="hullG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2c3038"/><stop offset="1" stop-color="#0e1014"/></linearGradient>
<linearGradient id="capG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#30353f"/><stop offset=".5" stop-color="#16191f"/><stop offset="1" stop-color="#07080b"/></linearGradient>
<linearGradient id="trailR" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ff2d3d" stop-opacity="0"/><stop offset="1" stop-color="#ff5a4a" stop-opacity=".6"/></linearGradient>
<linearGradient id="trailB" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5cc8ff" stop-opacity="0"/><stop offset="1" stop-color="#9fe0ff" stop-opacity=".35"/></linearGradient>
<radialGradient id="plume"><stop offset="0" stop-color="#ff4a3a" stop-opacity=".35"/><stop offset="1" stop-color="#ff1a2e" stop-opacity="0"/></radialGradient>
<radialGradient id="engR"><stop offset="0" stop-color="#fff0ea"/><stop offset=".35" stop-color="#ff4a3a"/><stop offset="1" stop-color="#ff1a2e" stop-opacity="0"/></radialGradient>
<radialGradient id="engB"><stop offset="0" stop-color="#f0fbff"/><stop offset=".35" stop-color="#5cc8ff"/><stop offset="1" stop-color="#1a8cff" stop-opacity="0"/></radialGradient>
<radialGradient id="boomG"><stop offset="0" stop-color="#fff2d8"/><stop offset=".35" stop-color="#ff9a4a"/><stop offset=".7" stop-color="#e2302a" stop-opacity=".6"/><stop offset="1" stop-color="#7a1010" stop-opacity="0"/></radialGradient>
<radialGradient id="planetG" cx="30%" cy="25%" r="80%"><stop offset="0" stop-color="#7a1a16"/><stop offset=".45" stop-color="#3a0a0d"/><stop offset=".8" stop-color="#140306"/><stop offset="1" stop-color="#060103"/></radialGradient>
<radialGradient id="shadeG" cx="64%" cy="70%" r="80%"><stop offset="0" stop-color="#020203" stop-opacity=".97"/><stop offset=".62" stop-color="#020203" stop-opacity=".9"/><stop offset=".85" stop-color="#020203" stop-opacity=".45"/><stop offset="1" stop-color="#020203" stop-opacity="0"/></radialGradient>
<radialGradient id="atmoGlow"><stop offset=".8" stop-color="#ff2a1a" stop-opacity="0"/><stop offset=".86" stop-color="#ff2a1a" stop-opacity=".32"/><stop offset=".92" stop-color="#ff2a1a" stop-opacity=".1"/><stop offset="1" stop-color="#ff2a1a" stop-opacity="0"/></radialGradient>
<radialGradient id="spill"><stop offset="0" stop-color="#ff2a2a" stop-opacity=".5"/><stop offset="1" stop-color="#ff2a2a" stop-opacity="0"/></radialGradient>
<radialGradient id="fogG"><stop offset="0" stop-color="#5a1418" stop-opacity=".55"/><stop offset="1" stop-color="#2a0608" stop-opacity="0"/></radialGradient>
<radialGradient id="visorG"><stop offset="0" stop-color="#ff3030" stop-opacity=".75"/><stop offset="1" stop-color="#ff1010" stop-opacity="0"/></radialGradient>
<radialGradient id="bladeHalo"><stop offset="0" stop-color="#ff2a3a" stop-opacity=".42"/><stop offset=".6" stop-color="#ff1a2a" stop-opacity=".12"/><stop offset="1" stop-color="#ff1a2a" stop-opacity="0"/></radialGradient>
<linearGradient id="capeG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0c0c11"/><stop offset=".6" stop-color="#050507"/><stop offset="1" stop-color="#120608"/></linearGradient>
<linearGradient id="armorG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22232b"/><stop offset=".6" stop-color="#0b0b0e"/><stop offset="1" stop-color="#100709"/></linearGradient>
<linearGradient id="helmG" x1="0" y1="0" x2="1" y2=".6"><stop offset="0" stop-color="#2a2c35"/><stop offset=".5" stop-color="#0d0e12"/><stop offset="1" stop-color="#1c0b0d"/></linearGradient>
<linearGradient id="deckG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d0d11"/><stop offset="1" stop-color="#040405"/></linearGradient>
<clipPath id="planetClip"><circle r="290"/></clipPath>
"""

svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">'
    f'<style>{STYLE}{LORD_CSS}</style><defs>{DEFS}{LORD_DEFS}</defs>'
    f'<rect width="{W}" height="{H}" fill="url(#space)"/>'
    '<ellipse class="neb" cx="1150" cy="220" rx="780" ry="340" fill="url(#nebR)"/>'
    '<ellipse class="neb2" cx="380" cy="760" rx="680" ry="320" fill="url(#nebD)"/>'
    '<ellipse class="neb2" cx="700" cy="430" rx="540" ry="150" fill="url(#nebR)" opacity=".4"/>'
    f'<g class="drift-far">{far}</g>'
    f'<g>{GALAXY}</g>'
    f'<g class="drift-mid">{mid}</g>'
    f'<g transform="translate(0,330) scale(.3)" opacity=".5"><g class="capfar">{CAP_FAR}</g></g>'
    + flash(880, 300, -0.2, 1.1) + flash(420, 250, -4.5) + flash(960, 95, -8.5, .8) + flash(620, 640, -2.5, .9)
    + jump(1320, 330, -0.3) + jump(470, 560, -9.3)
    + planet()
    + '<g class="capPos"><g transform="translate(0,150)"><g class="capmove">'
    f'<g transform="translate(840,-70) scale(.85)">{ESC}</g><g transform="translate(-190,74) scale(.7)">{ESC}</g>{CAP}'
    '</g></g></g>'
    # squadron A: three fleet fighters crossing left to right, firing
    '<g class="sqA"><g transform="rotate(6.1)">'
    f'<g>{FIGHTER}{bolts(0)}</g>'
    f'<g transform="translate(-60,-42)">{FIGHTER}{bolts(-.5)}</g>'
    f'<g transform="translate(-60,42)">{FIGHTER}{bolts(-1)}</g>'
    '</g></g>'
    # squadron D: a pair high up
    '<g class="sqD" opacity=".6"><g transform="rotate(2.8) scale(.7)">'
    f'<g>{FIGHTER}{bolts(-.3)}</g><g transform="translate(-54,30)">{FIGHTER}{bolts(-.8)}</g>'
    '</g></g>'
    # squadron B: two interceptors fleeing; the trailing one is hit and explodes
    '<g class="sqB"><g transform="rotate(183.1) scale(.85)" opacity=".8">'
    f'<g>{INTERCEPTOR}</g>'
    f'<g transform="translate(-46,34)"><g class="doomed">{INTERCEPTOR}</g>'
    '<g class="kill"><circle r="22" fill="url(#boomG)"/><circle r="14" fill="none" stroke="#ffb36b" stroke-width="1.6"/></g></g>'
    '</g></g>'
    # squadron C: fleet fighters hunting them
    f'<g class="sqC"><g transform="rotate(183.1)"><g>{FIGHTER}{bolts(-.2)}</g><g transform="translate(-50,-36)">{FIGHTER}{bolts(-.9)}</g></g></g>'
    + DECK + WARLORD +
    f'<g class="drift-near">{near}</g>'
    f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    '</svg>'
)

base = sys.argv[1] if len(sys.argv) > 1 else '.'
open(f'{base}/fleet.svg', 'w').write(svg)
assert '`' not in svg and '${' not in svg
assert len(svg) < 131072, len(svg)
if len(sys.argv) > 2:
    open(sys.argv[2], 'w').write(
        '// Night Fleet: an original dark space-opera battle. Generated by gen_fleet.py.\n'
        f'export const SCENE = `{svg}`\n')
print('chars', len(svg))
